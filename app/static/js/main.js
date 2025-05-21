// 文件上传相关功能
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const uploadButton = document.getElementById('upload-button');
    const loadingIndicator = document.getElementById('loading-indicator');
    const errorMessage = document.getElementById('error-message');
    const successMessage = document.getElementById('success-message');

    // 处理文件选择，显示预览
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;

        // 清除之前的消息
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';

        // 验证文件格式
        const validFormats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.heic', '.heif'];
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        if (!validFormats.includes(extension)) {
            errorMessage.textContent = `不支持的文件格式。支持的格式：${validFormats.join(', ')}`;
            errorMessage.style.display = 'block';
            fileInput.value = '';
            return;
        }

        // 显示预览
        const reader = new FileReader();
        reader.onload = function(e) {
            previewContainer.innerHTML = `
                <img src="${e.target.result}" alt="Preview" style="width:160px;height:160px;object-fit:contain;" class="mx-auto rounded-lg shadow-md border border-gray-200"/>
            `;
            previewContainer.style.display = 'block';
            uploadButton.disabled = false;
        };
        reader.readAsDataURL(file);
    });

    // 处理文件上传
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            errorMessage.textContent = '请选择要上传的图片';
            errorMessage.style.display = 'block';
            return;
        }

        // 显示加载指示器
        loadingIndicator.style.display = 'block';
        uploadButton.disabled = true;
        errorMessage.style.display = 'none';
        successMessage.style.display = 'none';

        // 创建 FormData 对象
        const formData = new FormData();
        formData.append('file', file);

        try {
            // 发送上传请求
            const response = await fetch('/api/v1/upload/', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (result.success) {
                successMessage.textContent = '图片上传成功！';
                successMessage.style.display = 'block';
                // 可以在这里添加其他成功后的操作，比如显示上传后的图片URL等
            } else {
                throw new Error(result.message || '上传失败');
            }
        } catch (error) {
            errorMessage.textContent = error.message || '上传过程中发生错误';
            errorMessage.style.display = 'block';
            previewContainer.style.display = 'none';
        } finally {
            loadingIndicator.style.display = 'none';
            uploadButton.disabled = false;
        }
    });

    // 拖放上传支持
    const dropZone = document.getElementById('drop-zone');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
        dropZone.classList.add('border-blue-500', 'bg-blue-50');
    }

    function unhighlight(e) {
        dropZone.classList.remove('border-blue-500', 'bg-blue-50');
    }

    dropZone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const file = dt.files[0];
        
        fileInput.files = dt.files;
        // 触发 change 事件，这样就会自动处理预览等逻辑
        fileInput.dispatchEvent(new Event('change'));
    }
});
