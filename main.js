// Update displayed threshold value when slider moves
document.getElementById('threshold').oninput = function () {
    document.getElementById('thresholdValue').innerText = this.value;
};

// Handle form submission
document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const res = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    const data = await res.json();
    const framesDiv = document.getElementById('frames');
    framesDiv.innerHTML = '';

    data.frames.forEach(obj => {
        const div = document.createElement('div');
        div.classList.add('frame-box');

        div.innerHTML = `
        <img src="/uploads/${obj.filename}" width="200">
        Clarity: ${obj.clarity}<br>
        Time: ${obj.timestamp} sec<br>
        <input type="checkbox" value="${obj.filename}" name="selectFrame">
      `;

        framesDiv.appendChild(div);
    });

    if (data.video) {
        const link = document.createElement('a');
        link.href = `/uploads/${data.video}`;
        link.innerText = 'Download Combined Video';
        link.style.display = 'block';
        link.style.marginTop = '20px';
        framesDiv.appendChild(link);
    }
});

// Handle download selected
async function downloadSelected() {
    const selected = Array.from(document.querySelectorAll('input[name="selectFrame"]:checked'))
        .map(cb => cb.value);

    const res = await fetch('/download-selected', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ files: selected })
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'selected_frames.zip';
    a.click();
}
