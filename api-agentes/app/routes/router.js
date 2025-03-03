import express from "express";
import {
    extractGenericData,
    callSpecializedAgents,
    transcribeText,
} from "../middleware/agentsMiddleware.js";

const agentsRouter = express.Router();
agentsRouter.use(express.json());

//                 /NomeDoAgente/AçãoDoAgente
agentsRouter.post(
    "/escrivao/transcrever",
    transcribeText,
    extractGenericData,
    callSpecializedAgents
);

export { agentsRouter };
