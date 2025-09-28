
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme');
    const compressionForm = document.getElementById('compression-form');
    const uploadSection = document.getElementById('upload-section');
    const previewSection = document.getElementById('preview-section');
    const fileInput = document.getElementById('file-input');
    const dropArea = document.getElementById('drop-area');
    const imagePreview = document.getElementById('image-preview');
    const fileSizeInfo = document.getElementById('file-size-info');
    const qualitySlider = document.getElementById('quality-slider');
    const kValueDisplay = document.getElementById('k-value-display');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultSection = document.getElementById('result-section');
    const compressedImage = document.getElementById('compressed-image');
    const compressedSizeInfo = document.getElementById('compressed-size-info');
    const downloadBtn = document.getElementById('download-btn');
    let uploadedFile = null;

    if (currentTheme) {
        document.body.classList.add(currentTheme);
        if (currentTheme === 'dark-mode') {
            themeToggle.checked = true;
        }
    }

    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.body.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            document.body.classList.remove('dark-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });

    function updateFileSizeDisplay() {
        if (!uploadedFile) return;

        let fileSize;
        let unit;

        if (uploadedFile.size < 1024 * 1024) { // Less than 1 MB
            fileSize = (uploadedFile.size / 1024).toFixed(2);
            unit = 'KB';
        } else { // 1 MB or more
            fileSize = (uploadedFile.size / 1024 / 1024).toFixed(2);
            unit = 'MB';
        }
        fileSizeInfo.textContent = `Original size: ${fileSize} ${unit}`;
    }

    function handleFile(file) {
        if (!file || !file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
        }

        uploadedFile = file;

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // Show file size
        updateFileSizeDisplay();

        // Switch views
        uploadSection.classList.add('hidden');
        previewSection.classList.remove('hidden');
    }

    // Handle file selection from input
    fileInput.addEventListener('change', (event) => {
        if (event.target.files.length > 0) {
            handleFile(event.target.files[0]);
        }
    });

    // Drag and Drop listeners
    dropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', () => {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dropArea.classList.remove('dragover');
        if (event.dataTransfer.files.length > 0) {
            // Update the file input's files
            fileInput.files = event.dataTransfer.files;
            handleFile(event.dataTransfer.files[0]);
        }
    });

    // Update the displayed k value when the slider is moved
    qualitySlider.addEventListener('input', (event) => {
        kValueDisplay.textContent = event.target.value;
    });

    // Handle form submission
    compressionForm.addEventListener('submit', function(event) {
        // Prevent the default form submission which reloads the page
        event.preventDefault();

        // Show loading indicator and hide previous result
        loadingIndicator.classList.remove('hidden');
        downloadBtn.classList.add('hidden');
        resultSection.classList.add('hidden');
        // Get the current value from the slider
        const kValue = qualitySlider.value;

        // Create a FormData object to send the file and k-value
        const formData = new FormData();
        formData.append('image', uploadedFile);
        formData.append('k', kValue);

        // Use fetch to send the data to the server
        fetch('/compress', {
            method: 'POST',
            body: formData
        })
        // First .then(): Parse the server's response as JSON
        .then(response => response.json())
        // Second .then(): Handle the parsed data
        .then(data => {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');

            // Set the src of the compressed image tag to the Base64 string
            compressedImage.src = data.image_data;
            // Update the text with the new file size
            compressedSizeInfo.textContent = `Compressed size: ${data.compressed_size_kb} KB`;
            // Set the href for the download button
            downloadBtn.href = data.image_data;
            // Show the result section
            resultSection.classList.remove('hidden');
            // Show the download button
            downloadBtn.classList.remove('hidden');
        });
    });
});