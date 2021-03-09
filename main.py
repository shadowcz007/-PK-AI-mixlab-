from sanic import Sanic
from sanic import response
from sanic.exceptions import NotFound


from camera import Camera

  
app = Sanic(name=__name__)
camera = Camera()

@app.route('/')
def handle_request(request):
    return response.html('<p>Hello world!</p><img src="/camera-stream/">')

@app.route('/test')
async def test(request):
    # print(camera.depth_estimation)
    return response.json({'hello': 'world'})

@app.route('/depth_estimation')
async def handle_depth_estimation(request):
    return await response.file_stream(camera.depth_estimation_file)

@app.route('/camera-stream/')
async def camera_stream(request):
    return response.stream(
        camera.stream,
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == '__main__':
    app.error_handler.add(
        NotFound,
        lambda r, e: response.empty(status=404)
    )
    app.run(host='0.0.0.0', port=8891)