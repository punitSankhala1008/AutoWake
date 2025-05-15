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

// this is new one

// const { app, BrowserWindow } = require("electron");
// const { spawn } = require("child_process");
// const path = require("path");

// let mainWindow;
// let flaskProcess;

// function createWindow() {
//   mainWindow = new BrowserWindow({
//     width: 800,
//     height: 600,
//     webPreferences: {
//       nodeIntegration: true,
//       contextIsolation: false,
//     },
//   });
//   mainWindow.loadFile("index.html");
//   // mainWindow.webContents.openDevTools(); // Uncomment for debugging
//   mainWindow.on("closed", () => {
//     mainWindow = null;
//   });
// }

// app.on("ready", () => {
//   flaskProcess = spawn("python", [
//     path.join(__dirname, "../Flask-Backend/server.py"),
//   ]);
//   flaskProcess.stdout.on("data", (data) => {
//     console.log(`Flask: ${data}`);
//   });
//   flaskProcess.stderr.on("data", (data) => {
//     console.error(`Flask Error: ${data}`);
//   });
//   setTimeout(createWindow, 3000); // Wait for Flask to start
// });

// app.on("window-all-closed", () => {
//   if (process.platform !== "darwin") {
//     app.quit();
//   }
// });

// app.on("quit", () => {
//   if (flaskProcess) {
//     flaskProcess.kill();
//   }
// });

// const { app, BrowserWindow } = require("electron");
// const { spawn } = require("child_process");
// const path = require("path");

// let mainWindow;
// let flaskProcess;

// function createWindow() {
//   mainWindow = new BrowserWindow({
//     width: 800,
//     height: 600,
//     webPreferences: {
//       nodeIntegration: true,
//       contextIsolation: false,
//     },
//   });
//   mainWindow.loadFile("index.html");
//   // mainWindow.webContents.openDevTools(); // Uncomment for debugging
//   mainWindow.on("closed", () => {
//     mainWindow = null;
//   });
// }

// app.on("ready", () => {
//   flaskProcess = spawn("python", [
//     path.join(__dirname, "../Flask-Backend/server1.py"),
//   ]);
//   flaskProcess.stdout.on("data", (data) => {
//     console.log(`Flask: ${data}`);
//   });
//   flaskProcess.stderr.on("data", (data) => {
//     console.error(`Flask Error: ${data}`);
//   });
//   setTimeout(createWindow, 3000);
// });

// app.on("window-all-closed", () => {
//   if (process.platform !== "darwin") {
//     app.quit();
//   }
// });

// app.on("quit", () => {
//   if (flaskProcess) {
//     flaskProcess.kill();
//   }
// });

// electron-ui/main.js
// electron-ui/main.js

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

  // Load your HTML UI
  mainWindow.loadFile(path.join(__dirname, "index.html"));

  // Open DevTools for debugging (comment out in production)
  mainWindow.webContents.openDevTools();

  mainWindow.on("closed", () => {
    mainWindow = null;
  });
}

app.on("ready", () => {
  // 1. Start the Flask backend
  const serverPath = path.join(__dirname, "..", "Flask-Backend", "server1.py");
  flaskProcess = spawn("python", [serverPath]);

  flaskProcess.stdout.on("data", (data) => {
    console.log(`Flask: ${data}`);
  });

  flaskProcess.stderr.on("data", (data) => {
    console.error(`Flask Error: ${data}`);
  });

  flaskProcess.on("exit", (code, signal) => {
    console.log(`Flask process exited with code ${code} and signal ${signal}`);
  });

  // 2. Delay window creation for a few seconds to let Flask start
  setTimeout(createWindow, 3000);
});

app.on("window-all-closed", () => {
  // On macOS it’s common for apps to stay open until Cmd+Q
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", () => {
  // Clean up the Flask process
  if (flaskProcess) {
    flaskProcess.kill();
  }
});

app.on("activate", () => {
  // On macOS re-create a window when dock icon is clicked
  if (mainWindow === null) {
    createWindow();
  }
});
