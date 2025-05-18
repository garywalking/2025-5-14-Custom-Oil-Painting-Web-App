"""
主应用测试文件
测试基础API端点是否正常工作
"""

def test_read_main(test_client):
    """测试根路由"""
    response = test_client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_static_files(test_client):
    """测试静态文件是否可以访问"""
    response = test_client.get("/static/css/styles.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]