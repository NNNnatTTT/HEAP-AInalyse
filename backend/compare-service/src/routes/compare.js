// compare-service/src/routes/compare.js
import express from 'express';
import multer from 'multer';
import FormData from 'form-data';
import fetch from 'node-fetch';

const router = express.Router();
const upload = multer();

router.post('/', upload.fields([
  { name: 'fileA' },
  { name: 'fileB' }
]), async (req, res) => {
  try {
    const [fileA, fileB] = [req.files.fileA[0], req.files.fileB[0]];

    // helper to call your scanner microservice
    async function scan(file) {
      const form = new FormData();
      form.append('file', file.buffer, file.originalname);
      const r = await fetch('http://localhost:9697/scan_document', {
        method: 'POST',
        body: form,
        headers: form.getHeaders()
      });
      if (!r.ok) throw new Error('Scanner error: ' + await r.text());
      return await r.json();
    }

    // 1) scan both PDFs
    const [jsonA, jsonB] = await Promise.all([
      scan(fileA),
      scan(fileB)
    ]);

    // 2) send to your AI prompt service
    const promptResp = await fetch('http://localhost:3000/api/gemini', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        mode: 'compare',
        contractData: { contract1: jsonA, contract2: jsonB }
      })
    });
    if (!promptResp.ok) throw new Error('Prompt error: ' + await promptResp.text());
    const result = await promptResp.json();

    // 3) return combined result
    res.json(result);

  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message });
  }
});

export default router;
