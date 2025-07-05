const express = require('express');
const multer = require('multer');
const controller = require('../controllers/geminiController');

const upload = multer({ storage: multer.memoryStorage() });
const router = express.Router();

// expects fields fileA and fileB
router.post(
  '/',
  upload.fields([
    { name: 'fileA', maxCount: 1 },
    { name: 'fileB', maxCount: 1 }
  ]),
  controller.compare
);

module.exports = router;
