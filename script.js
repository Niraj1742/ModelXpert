document.getElementById('uploadBtn').addEventListener('click', async () => {
    const file = document.getElementById('dataset').files[0];
    if (!file) {
      alert('Please upload a dataset.');
      return;
    }
  
    const formData = new FormData();
    formData.append('file', file);
  
    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  });
  
  document.getElementById('preprocessBtn').addEventListener('click', async () => {
    const missingValues = document.getElementById('missingValues').value;
  
    try {
      const response = await fetch('/preprocess', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ missingValues }),
      });
      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error preprocessing data:', error);
    }
  });
  
  document.getElementById('trainBtn').addEventListener('click', async () => {
    const modelType = document.getElementById('modelType').value;
  
    try {
      const response = await fetch('/train', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ modelType }),
      });
      const data = await response.json();
      document.getElementById('results').innerText = JSON.stringify(data, null, 2);
    } catch (error) {
      console.error('Error training model:', error);
    }
  });
