// ← none of this section changes:
export async function Prompt(mode, contractData) {
    const response = await fetch('http://localhost:3000/api/gemini', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ mode, contractData })
    });
  
    if (!response.ok) throw new Error('Gemini API call failed');
    return await response.json();
  }
  
  // ── ADD THIS AT THE BOTTOM OF api/Prompt.js ──
  /**
   * Send raw file uploads via FormData
   * (leaves your JSON/text Prompt() intact above)
   */
  export async function sendComparePrompt(formData) {
    const response = await fetch('http://localhost:3000/api/gemini', {
      method: 'POST',
      body: formData
    });
  
    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`Gemini API call failed (${response.status}): ${errText}`);
    }
    return await response.json();
  }
  