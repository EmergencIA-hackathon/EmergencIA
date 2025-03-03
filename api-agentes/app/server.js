import express from "express";
import { agentsRouter } from "./routes/router.js";
import cors from "cors";

const app = express();

app.use(express.json());
app.use(cors());
app.use("/api/agentes", agentsRouter);

app.get("", (req, res) => {
    console.log("OKAY");
    res.sendStatus(200);
});

const PORT = process.env.BACKEND_PORT;
app.listen(PORT, () => {
    console.log(`Listening at port: ${PORT}`);
});
