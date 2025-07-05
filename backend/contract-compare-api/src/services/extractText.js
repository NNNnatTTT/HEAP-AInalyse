const pdf = require('pdf-parse');
const mammoth = require('mammoth');

module.exports = async (buffer, mimeType) => {
  if (mimeType === 'application/pdf') {
    const data = await pdf(buffer);
    return data.text;
  }

  if (
    mimeType === 'application/msword' ||
    mimeType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
  ) {
    const { value } = await mammoth.extractRawText({ buffer });
    return value;
  }

  throw new Error(`Unsupported file type: ${mimeType}`);
};
