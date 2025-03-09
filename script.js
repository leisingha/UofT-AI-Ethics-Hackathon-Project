document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.checklist-form');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get all checkboxes (not just checked ones)
        const checkboxes = document.querySelectorAll('.lcheck');
        
        // Create binary array from checkbox states
        const inputData = Array.from(checkboxes).map(box => box.checked ? 1 : 0);
        
        try {
            // Send data to Python server
            const response = await fetch('http://localhost:5500/analyze_learning_style', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ input_data: inputData })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            // Redirect to the appropriate learning path
            const learningPaths = {
                0: 'visual-learning.html',
                1: 'auditory-learning.html',
                2: 'kinesthetic-learning.html',
                3: 'analytical-learning.html'
            };
            
            window.location.href = learningPaths[result.learning_style];
            
        } catch (error) {
            console.error('Error:', error);
            alert('There was an error analyzing your learning style. Please try again.');
        }
    });
}); 