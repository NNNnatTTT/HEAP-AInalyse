const extractText = require('../services/extractText');
const compareContracts = require('../services/compareContracts');

exports.compare = async (req, res) => {
  try {
    const files = req.files;
    if (!files?.fileA?.[0] || !files?.fileB?.[0]) {
      return res.status(400).json({ error: 'Both fileA and fileB are required.' });
    }

    const fileA = files.fileA[0];
    const fileB = files.fileB[0];

    const textA = await extractText(fileA.buffer, fileA.mimetype);
    const textB = await extractText(fileB.buffer, fileB.mimetype);

    const result = await compareContracts(textA, textB);
    return res.json({ text: result });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message });
  }
};
