document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('chatForm');
    const input = document.getElementById('queryInput');
    const chatWindow = document.getElementById('chatWindow');
  
    function appendMessage(text, className) {
      const msgDiv = document.createElement('div');
      msgDiv.className = `message ${className}`;
      msgDiv.textContent = text;
      chatWindow.appendChild(msgDiv);
      chatWindow.scrollTop = chatWindow.scrollHeight;
    }
  
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const query = input.value.trim();
      if (!query) return;
  
      appendMessage(query, 'user-msg');
      input.value = '';
      input.disabled = true;
  
      try {
        const res = await fetch('/employee/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query })
        });
        const data = await res.json();
        appendMessage(data.response || 'No response.', 'bot-msg');
      } catch (err) {
        appendMessage('Error communicating with server.', 'bot-msg');
      } finally {
        input.disabled = false;
        input.focus();
      }
    });
  });
  