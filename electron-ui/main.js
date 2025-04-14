// // main.js
// const { app, BrowserWindow } = require("electron");
// const path = require("path");

// function createWindow() {
//   const win = new BrowserWindow({
//     width: 800,
//     height: 600,
//     webPreferences: {
//       nodeIntegration: true, // Enable Node integration for renderer.js
//       contextIsolation: false, // For simplicity; in production consider using preload scripts
//     },
//   });

//   win.loadFile("index.html");
// }

// app.whenReady().then(createWindow);

// app.on("window-all-closed", () => {
//   if (process.platform !== "darwin") {
//     app.quit();
//   }
// });

// app.on("activate", () => {
//   if (BrowserWindow.getAllWindows().length === 0) {
//     createWindow();
//   }
// });

const { app, BrowserWindow } = require("electron");
const { spawn } = require("child_process");
const path = require("path");

let mainWindow;
let flaskProcess;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });
  mainWindow.loadFile("index.html");
  // mainWindow.webContents.openDevTools(); // Uncomment for debugging
  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.on("ready", () => {
  flaskProcess = spawn("python", [
    path.join(__dirname, "../Flask-Backend/server.py"),
  ]);
  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });
  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask Error: ${data}`);
  });
  setTimeout(createWindow, 3000); // Wait for Flask to start
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("quit", () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
});
