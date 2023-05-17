function countWords() {
  const text = textarea.value.trim();
  const words = text ? text.split(/\s+/) : [];
  return words.length;
}

const textarea = document.querySelector('#answer');
const count = document.querySelector('#count');
const submitButton = document.querySelector('form[action="/score"] button[type="submit"]');
const loaderContainer = document.querySelector('.loader-container');

textarea.addEventListener('input', () => {
  const wordCount = countWords();
  count.textContent = `${wordCount} words`;
});

count.textContent = `${countWords()} words`;

submitButton.addEventListener('click', async (event) => {
  event.preventDefault();

  loaderContainer.style.display = 'flex';
  
  try {
    const response = await fetch('/score', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        answer: textarea.value,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }

    const data = await response.json();

    loaderContainer.style.display = 'none';

    if (data.status === 'success') {
      window.location.href = '/results';
    }
  } catch (error) {
    console.error('Error:', error);
    alert('An error occurred. Please try again.');
    
    loaderContainer.style.display = 'none';
  }
});
