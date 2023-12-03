import argparse
import asyncio
import json
import logging
import os
import re
import subprocess
from concurrent import futures
from typing import Iterator

import ffmpeg
import redis
from grpc import ServicerContext
from grpc import server as grpc_server
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from playwright._impl._api_types import TimeoutError
from playwright.async_api import ElementHandle, Page, async_playwright

from llmstack.common.runner.display import VirtualDisplayPool
from llmstack.common.runner.proto import runner_pb2
from llmstack.common.runner.proto.runner_pb2 import (
    TERMINATE,
    BrowserButton,
    BrowserContent,
    BrowserInputField,
    BrowserLink,
    BrowserSelectField,
    BrowserTextAreaField,
    PlaywrightBrowserRequest,
    PlaywrightBrowserResponse,
    RemoteBrowserRequest,
    RemoteBrowserResponse,
    RemoteBrowserSession,
    RemoteBrowserState,
)
from llmstack.common.runner.proto.runner_pb2_grpc import (
    RunnerServicer,
    add_RunnerServicer_to_server,
)

logger = logging.getLogger(__name__)


async def get_browser_content_from_page(page) -> BrowserContent:
    content = BrowserContent()
    content.url = page.url
    content.title = await page.title()
    content.text = await page.inner_text('body')

    try:
        buttons = await page.locator('button').all()
        nth = 0
        for button in buttons[:50]:
            content.buttons.append(BrowserButton(
                text=(await button.text_content()).strip(),
                selector=f'button >> nth={nth}',
            ))
            nth += 1
    except Exception as e:
        logger.exception(e)
        pass

    try:
        inputs = await page.locator('input').all()
        for input in inputs[:50]:
            nth = 0
            input_type = await input.get_attribute('type')
            if input_type == 'submit':
                content.buttons.append(BrowserButton(
                    text=(await input.text_content()).strip(),
                    selector=f'input >> nth={nth}',
                ))
            else:
                content.inputs.append(BrowserInputField(
                    text=(await input.text_content()).strip(),
                    selector=f'input >> nth={nth}',
                ))
            nth += 1
    except Exception as e:
        logger.exception(e)
        pass

    try:
        selects = await page.locator('select').all()
        nth = 0
        for select in selects[:50]:
            content.selects.append(BrowserSelectField(
                text=(await select.text_content()).strip(),
                selector=f'select >> nth={nth}',
            ))
            nth += 1
    except Exception as e:
        logger.exception(e)
        pass

    try:
        textareas = await page.locator('textarea').all()
        nth = 0
        for textarea in textareas[:50]:
            content.textareas.append(BrowserTextAreaField(
                text=(await textarea.text_content()).strip(),
                selector=f'textarea >> nth={nth}',
            ))
            nth += 1
    except Exception as e:
        logger.exception(e)
        pass

    try:
        links = await page.locator('a').all()
        nth = 0
        for link in links[:100]:
            content.links.append(BrowserLink(
                text=(await link.text_content()).strip(),
                selector=f'a >> nth={nth}',
                url=await link.get_attribute('href'),
            ))
            nth += 1
    except Exception as e:
        logger.exception(e)
        pass

    return content


class Runner(RunnerServicer):
    def __init__(self, display_pool: VirtualDisplayPool = None):
        super().__init__()
        self.display_pool = display_pool

    async def _process_remote_browser_input_stream(self, request_iterator: Iterator[RemoteBrowserRequest], display, request: RemoteBrowserRequest):
        os.environ['DISPLAY'] = f'{display["DISPLAY"]}.0'
        logger.info(f"Using {os.environ['DISPLAY']}")
        session_data = None
        terminate = False
        async with async_playwright() as playwright:
            try:
                session_data = json.loads(
                    request.init_data.session_data) if request.init_data.session_data else None
                browser = await playwright.chromium.launch(headless=False)
                context = await browser.new_context(no_viewport=True, storage_state=session_data)
                page = await context.new_page()

                # Create an async task for waiting for the URL pattern
                page_load_task = asyncio.create_task(
                    page.wait_for_url(
                        re.compile(
                            request.init_data.terminate_url_pattern or 'chrome://newtab'),
                        timeout=request.init_data.timeout*1000
                    )
                )

                # Navigate to the initial URL
                await page.goto(request.init_data.url or 'chrome://newtab')

                for next_request in request_iterator:
                    if next_request is not None:
                        if next_request.input.type == TERMINATE:
                            raise Exception(
                                'Terminating browser because of timeout')
                    else:
                        # Sleep a bit to prevent a busy loop that consumes too much CPU
                        await asyncio.sleep(0.1)

                    if page_load_task.done():
                        break

                # Wait for the page load task to complete
                if not page_load_task.done():
                    await page_load_task

            except TimeoutError:
                pass
            except Exception as e:
                logger.exception(e)
                terminate = True
            finally:
                # Stop page load task if still running
                if not page_load_task.done():
                    page_load_task.cancel()

                if request.init_data.persist_session and (page_load_task.done() or not request.init_data.terminate_url_pattern):
                    session_data = await context.storage_state()

                # Clean up
                await context.close()
                await browser.close()

                if terminate:
                    raise Exception('Terminating browser')

        return session_data

    def GetRemoteBrowser(self, request_iterator: Iterator[RemoteBrowserRequest], context: ServicerContext) -> Iterator[RemoteBrowserResponse]:
        # Get input from the client
        request = next(request_iterator)

        # Get a display from the pool and send its info to the client
        display = self.display_pool.get_display(remote_control=True)
        wss_server_path = f'{self.wss_hostname}:{self.wss_port}' if '/' not in self.wss_hostname else self.wss_hostname

        # Return the display info to the client
        yield RemoteBrowserResponse(
            session=RemoteBrowserSession(
                ws_url=f"{'wss' if self.wss_secure else 'ws'}://{display['username']}:{display['password']}@{wss_server_path}?token={display['token']}",
            ),
            state=RemoteBrowserState.RUNNING,
        )

        # Use ThreadPoolExecutor to run the async function in a separate thread
        with futures.ThreadPoolExecutor() as executor:
            # Wrap the coroutine in a function that gets the current event loop or creates a new one
            def run_async_code(loop):
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(
                    self._process_remote_browser_input_stream(
                        request_iterator, display, request)
                )

            # Create a new event loop that will be run in a separate thread
            new_loop = asyncio.new_event_loop()
            # Submit the function to the executor and get a Future object
            future = executor.submit(run_async_code, new_loop)

            # Wait for the future to complete and get the return value
            try:
                session_state = future.result()
            except Exception as e:
                logger.error(e)
                session_state = None

        # Put the display back in the pool and return
        self.display_pool.put_display(display)
        yield RemoteBrowserResponse(
            state=RemoteBrowserState.TERMINATED,
            session=RemoteBrowserSession(
                session_data=json.dumps(
                    session_state) if session_state else '',
            ),
        )

    async def _process_playwright_request(self, page: Page, request):
        steps = list(request.steps)
        outputs = []
        logger.info(steps)

        for step in steps:
            if step.type == TERMINATE:
                raise Exception(
                    'Terminating browser because of timeout')
            elif step.type == runner_pb2.GOTO:
                await page.goto((page.url + step.data if step.data and step.data.startswith('/') else step.data) or page.url)
            elif step.type == runner_pb2.CLICK:
                locator = page.locator(step.selector)
                await locator.click()
            elif step.type == runner_pb2.WAIT:
                await page.wait_for_selector(step.selector or 'body', timeout=int(step.data)*1000 if step.data else 5000)
            elif step.type == runner_pb2.COPY:
                results = await page.query_selector_all(step.selector or 'body')
                outputs.append({
                    'url': page.url,
                    'text': "".join([await result.inner_text() for result in results]),
                })
            elif step.type == runner_pb2.TYPE:
                await page.type(step.selector, step.data)
            elif step.type == runner_pb2.SCROLL_X:
                await page.mouse.wheel(delta_x=int(step.data))
            elif step.type == runner_pb2.SCROLL_Y:
                await page.mouse.wheel(delta_y=int(step.data))

        return outputs

    async def _process_playwright_input_stream(self, initial_request, request_iterator, display, ffmpeg_process):
        os.environ['DISPLAY'] = f'{display["DISPLAY"]}.0'
        logger.info(f"Using {os.environ['DISPLAY']}")
        outputs = []
        content = BrowserContent()
        session_data = initial_request.session_data

        async with async_playwright() as playwright:
            try:
                session_data = json.loads(
                    session_data) if session_data else None
                browser = await playwright.chromium.launch(headless=False)
                context = await browser.new_context(no_viewport=True, storage_state=session_data)
                page = await context.new_page()

                url = initial_request.url
                if not url.startswith('http'):
                    url = f'https://{url}'

                # Load the start_url before processing the steps
                await page.goto(url, wait_until='domcontentloaded')

                outputs = await self._process_playwright_request(
                    page, initial_request)
                content = await get_browser_content_from_page(page)

                yield (outputs, content)

                for next_request in request_iterator:
                    outputs += await self._process_playwright_request(
                        page, next_request)
                    # Populate content from the last page
                    content = await get_browser_content_from_page(page)

                    yield (outputs, content)

                    await asyncio.sleep(0.1)

            except Exception as e:
                logger.exception(e)
            finally:
                # Clean up
                await browser.close()

                if ffmpeg_process:
                    ffmpeg_process.kill()

                yield (outputs, content)

    def GetPlaywrightBrowser(self, request_iterator: Iterator[PlaywrightBrowserRequest], context: ServicerContext) -> Iterator[PlaywrightBrowserResponse]:
        # Get the first request from the client
        initial_request = next(request_iterator)
        display = self.display_pool.get_display(remote_control=False)
        SENTINAL = object()

        if not display:
            yield PlaywrightBrowserResponse(state=RemoteBrowserState.TERMINATED)
            return

        # Start ffmpeg in a separate process to stream the display
        ffmpeg_process = (
            ffmpeg
            .input(f"{display['DISPLAY']}.0", format='x11grab', framerate=10, video_size=(1024, 720))
            .output('pipe:', format='mp4', vcodec='h264', movflags='faststart+frag_keyframe+empty_moov+default_base_moof', g=25, y=None)
            .run_async(pipe_stdout=True, pipe_stderr=True)
        ) if initial_request.stream_video else None

        # Use ThreadPoolExecutor to run the async function in a separate thread
        with futures.ThreadPoolExecutor(thread_name_prefix='async_tasks') as executor:
            browser_done = False
            video_done = False
            # Wrap the coroutine in a function that gets the current event loop or creates a new one

            def run_async_code(loop, fn):
                asyncio.set_event_loop(loop)

                return loop.run_until_complete(fn())

            # Create a queue to store the browser output
            content_queue = asyncio.Queue()

            # Create a queue to store browser video output
            video_queue = asyncio.Queue()

            async def collect_browser_content():
                async for (outputs, content) in self._process_playwright_input_stream(
                        initial_request, request_iterator, display, ffmpeg_process):
                    await content_queue.put((outputs, content))
                await content_queue.put(SENTINAL)

            async def read_video_output():
                while True and ffmpeg_process:
                    try:
                        chunk = ffmpeg_process.stdout.read(1024 * 3)
                        if len(chunk) == 0:
                            break
                        await video_queue.put(chunk)
                    except Exception as e:
                        logger.error(e)
                        break
                await video_queue.put(SENTINAL)

            # Start a task to read the video output from ffmpeg
            video_future = executor.submit(
                run_async_code, asyncio.new_event_loop(), read_video_output)

            # Submit the function to the executor and get a Future object
            content_future = executor.submit(
                run_async_code, asyncio.new_event_loop(), collect_browser_content)

            # Wait for the future to complete and get the return value
            try:
                yield PlaywrightBrowserResponse(state=RemoteBrowserState.RUNNING)

                while not browser_done and not video_done:
                    try:
                        item = content_queue.get_nowait()
                        if item is SENTINAL:
                            browser_done = True
                            break

                        (output_texts, content) = item
                        response = PlaywrightBrowserResponse(
                            state=RemoteBrowserState.RUNNING)

                        for output_text in output_texts:
                            response.outputs.append(runner_pb2.BrowserOutput(
                                text=output_text['text'], url=output_text['url']))
                        response.content.CopyFrom(content)

                        yield response
                    except asyncio.QueueEmpty:
                        pass

                    try:
                        chunk = video_queue.get_nowait()
                        if chunk is SENTINAL:
                            video_done = True
                            break
                        yield PlaywrightBrowserResponse(video=chunk)
                    except asyncio.QueueEmpty:
                        pass

                    if content_future.done() or video_future.done() or browser_done or video_done:
                        break

                yield PlaywrightBrowserResponse(
                    state=RemoteBrowserState.TERMINATED)
            except Exception as e:
                logger.error(e)
                yield PlaywrightBrowserResponse(
                    state=RemoteBrowserState.TERMINATED)
            finally:
                self.display_pool.put_display(display)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description='LLMStack runner service')
    parser.add_argument('--port', type=int,
                        help='Port to run the server on', default=50051)
    parser.add_argument('--host', type=str,
                        help='Host to run the server on', default='0.0.0.0')
    parser.add_argument('--max-displays', type=int,
                        help='Maximum number of virtual displays to use', default=5)
    parser.add_argument('--start-display', type=int,
                        help='Start display number number', default=99)
    parser.add_argument('--display-res', type=str,
                        help='Display resolution', default='1024x720x24')
    parser.add_argument('--rfb-start-port', type=int,
                        help='RFB start port', default=12000)
    parser.add_argument('--redis-host', type=str,
                        help='Redis host', default='localhost')
    parser.add_argument('--redis-port', type=int,
                        help='Redis port', default=6379)
    parser.add_argument('--redis-db', type=int,
                        help='Redis DB', default=0)
    parser.add_argument('--redis-password', type=str,
                        help='Redis password', default=None)
    parser.add_argument('--hostname', type=str,
                        help='Hostname for mapping remote browser', default='localhost')
    parser.add_argument('--wss-hostname', type=str,
                        help='Hostname for remote browser websocket', default='localhost')
    parser.add_argument('--wss-port', type=int,
                        help='Port for remote browser websocket', default=23100)
    parser.add_argument('--wss-secure', type=bool, default=False,
                        help='Secure remote browser websocket', action=argparse.BooleanOptionalAction)
    parser.add_argument('--playwright-port', type=int,
                        help='Port for playwright server. Disabled by default', default=-1)
    parser.add_argument
    parser.add_argument('--log-level', type=str,
                        help='Log level', default='INFO')
    args = parser.parse_args()

    # Read environment variables and override arguments
    args.port = int(os.getenv('RUNNER_PORT', args.port))
    args.host = os.getenv('RUNNER_HOST', args.host)
    args.max_displays = int(
        os.getenv('RUNNER_MAX_DISPLAYS', args.max_displays))
    args.start_display = int(
        os.getenv('RUNNER_START_DISPLAY', args.start_display))
    args.display_res = os.getenv('RUNNER_DISPLAY_RES', args.display_res)
    args.rfb_start_port = int(
        os.getenv('RUNNER_RFB_START_PORT', args.rfb_start_port))
    args.redis_host = os.getenv('RUNNER_REDIS_HOST', args.redis_host)
    args.redis_port = int(os.getenv('RUNNER_REDIS_PORT', args.redis_port))
    args.redis_password = os.getenv(
        'RUNNER_REDIS_PASSWORD', args.redis_password)
    args.redis_db = int(os.getenv('RUNNER_REDIS_DB', args.redis_db))
    args.hostname = os.getenv('RUNNER_HOSTNAME', args.hostname)
    args.wss_hostname = os.getenv('RUNNER_WSS_HOSTNAME', args.wss_hostname)
    args.wss_port = int(os.getenv('RUNNER_WSS_PORT', args.wss_port))
    args.wss_secure = os.getenv('RUNNER_WSS_SECURE', args.wss_secure)
    args.log_level = os.getenv('RUNNER_LOG_LEVEL', args.log_level)
    args.playwright_port = int(
        os.getenv('RUNNER_PLAYWRIGHT_PORT', args.playwright_port))

    # Configure logger
    logging.basicConfig(level=args.log_level)

    # Connect and verify redis
    redis_client = redis.Redis(
        host=args.redis_host, port=args.redis_port, db=args.redis_db, password=args.redis_password)
    redis_client.ping()

    # Start playwright server if port is specified
    playwright_process = None
    if args.playwright_port > 0:
        playwright_process = subprocess.Popen(['playwright', 'run-server',
                                               '--port', str(args.playwright_port)])

    display_pool = VirtualDisplayPool(
        redis_client, hostname=args.hostname, max_displays=args.max_displays,
        start_display=args.start_display, display_res=args.display_res,
        rfb_start_port=args.rfb_start_port)

    # Start websockify server
    websockify_process = subprocess.Popen(
        ['websockify', f'{args.wss_port}', '--web', '/usr/share/www/html',
         '--token-plugin=llmstack.common.runner.token.TokenRedis',
         f'--token-source={args.redis_host}:{args.redis_port}:{args.redis_db}{f":{args.redis_password}" if args.redis_password else ""}',
         '-v', '--auth-plugin=llmstack.common.runner.auth.BasicHTTPAuthWithRedis',
         f'--auth-source={args.redis_host}:{args.redis_port}:{args.redis_db}{f":{args.redis_password}" if args.redis_password else ""}'],
        close_fds=True)

    server = grpc_server(futures.ThreadPoolExecutor(
        max_workers=10, thread_name_prefix='grpc_workers'))
    runner = Runner(display_pool=display_pool)
    runner.wss_hostname = args.wss_hostname
    runner.wss_port = args.wss_port
    runner.wss_secure = args.wss_secure

    add_RunnerServicer_to_server(runner, server)

    # Add health checking service
    health_servicer = health.HealthServicer()
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    # Set the health status to SERVING
    health_servicer.set('', health_pb2.HealthCheckResponse.SERVING)

    server.add_insecure_port(f'[::]:{args.port}')
    server.start()

    logger.info(f"Server running at http://[::]:{args.port}")
    server.wait_for_termination()

    # Stop websockify and playwright servers
    websockify_process.kill()
    playwright_process.kill()


if __name__ == '__main__':
    main()
