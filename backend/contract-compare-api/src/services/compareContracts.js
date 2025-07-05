// Old:
// const { Configuration, OpenAIApi } = require('openai');
// const config = new Configuration({ apiKey: process.env.OPENAI_API_KEY });
// const client = new OpenAIApi(config);

// New:
const OpenAI = require("openai");
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: process.env.OPENAI_API_BASE_URL
});

module.exports = async (textA, textB) => {
  const prompt = `
Context:
Comparing key clauses between two employment contracts, using MOM key employment terms as background.

Role:
You are an employment lawyer advising your client.

Instruction:
Provide a clear and concise head-to-head comparison between the two contracts, focusing on these clauses:
1. Job Title
2. Job responsibilities and duties
3. Start Date
4. Working Hours
5. Compensation (General, Public Holiday and Overtime Pay)
6. Leaves
7. Benefits
8. Probationary period and termination clauses
9. Confidentiality and non-compete clauses

Output Format:
[Clause 1 Title]: [Contract A Summary], [Contract B Summary];
[Clause 2 Title]: [Contract A Summary], [Contract B Summary];
... and so on for all listed clauses.

--- Contract A ---
${textA}

--- Contract B ---
${textB}
  `.trim();

  const response = await openai.chat.completions.create({
    model: "google/gemini-2.0-flash-exp:free",
    messages: [{ role: "user", content: prompt }],
    temperature: 0.2,
    max_tokens: 1500
  });

  return response.choices[0].message.content.trim();
};
