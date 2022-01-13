require("dotenv").config();
const path = require("path");
const fs = require("fs").promises;
const cp = require("child_process");
const express = require("express");
const multer = require("multer");

const app = express();
const folder = "uploads";
//const upload = multer({storage: multer.memoryStorage()})
const upload = multer.diskStorage({
  destination: folder,
  filename: function (req, file, cb) {
    cb(null, "image" + +Date.now() + path.extname(file.originalname));
  },
});
app.use(express.json());
//app.post('/image', upload.single('image'), function (req, res){
app.post(
  "/image",
  multer({ storage: upload }).single("image"),
  function (req, res) {
    const py = cp.spawn("python", [
      //"./python/main.py",
      "./python/main_face_n_hands.py",
      req.file.filename /*, Buffer.from(req.file.buffer, 'base64')*/,
    ]);
    //py.stdin.write(Buffer.from(JSON.stringify(req.file.buffer)))
    py.stdin.end();
    let sent = false;
    py.stdout.on("data", function (data) {
      console.log("\x1b[0m", data.toString());
      if (sent) {
        return;
      }
      const img = Buffer.from(data, "base64");
      res.writeHead(200, {
        "Content-Type": "image/jpeg",
        "Content-Length": img.length,
      });
      //res.send({data: data.toString()});
      res.end(img);
      sent = true;
    });
    py.stdout.on("end", function () {
      fs.unlink(path.join(folder, req.file.filename));
      py.kill()
    });
    py.stderr.on("data", function (data) {
      const msg = data.toString()
      console.log("\x1b[31m", msg);
      if(/^info:/i.test(msg)){return;} //костыль
      if (sent) {
        return;
      }
      res.send({ data: msg });
      sent = true;
    });
  }
);
app.use("/", express.static(path.resolve(__dirname, "public")));
const port = process.env.PORT;
app.listen(port, function () {
  console.log("\x1b[36m", `Web server listening on port ${port}`);
});
