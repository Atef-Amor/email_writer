document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const emailForm = document.getElementById('emailForm');
    const generatedEmail = document.getElementById('generatedEmail');
    const emailDraft = document.getElementById('emailDraft');
    const contextUsed = document.getElementById('contextUsed');

    // Handle document upload
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fileInput = uploadForm.querySelector('input[type="file"]');
        const file = fileInput.files[0];
        
        if (!file) {
            alert('Please select a file to upload');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            if (response.ok) {
                alert('Document uploaded successfully!');
                fileInput.value = ''; // Clear the file input
            } else {
                alert('Error: ' + data.error);
            }
        } catch (error) {
            alert('Error uploading document: ' + error.message);
        }
    });

    // Handle email generation
    emailForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const recipient = document.getElementById('recipient').value;
        const subject = document.getElementById('subject').value;
        const context = document.getElementById('context').value;

        try {
            const response = await fetch('/compose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    recipient,
                    subject,
                    context
                })
            });
            
            const data = await response.json();
            if (response.ok) {
                // Display the generated email
                emailDraft.textContent = data.draft;
                contextUsed.textContent = data.context_used;
                generatedEmail.classList.remove('hidden');
            } else {
                alert('Error generating email: ' + data.error);
            }
        } catch (error) {
            alert('Error generating email: ' + error.message);
        }
    });
}); 