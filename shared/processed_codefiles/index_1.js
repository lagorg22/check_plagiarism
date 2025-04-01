const express = require("express");
const conectarDB = require("./config/db");
const cors = require('cors')
const app = express();
conectarDB();
app.use(cors())
app.use(express.json({ extended: true }));
const port = process.env.PORT || 4000;
app.use("/api/usuarios", require("./routes/usuarios.js"));
app.use("/api/auth", require("./routes/auth.js"));
app.use("/api/proyectos", require("./routes/proyectos.js"));
app.use("/api/tareas", require("./routes/tareas.js"));
app.get("/", (req, res) => {
res.send("Hola Mundo");
});
app.listen(port,'0.0.0.0', () => {
console.log(`El servidor está funcionando en el puerto ${port}`);
});