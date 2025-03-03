import { genericDataExtractionAgent } from "../agents/genericDataAgent.js";
import { scrivenerAgent } from "../agents/scrivenerAgent.js";
import {
    extractorAgentPromptTemplate,
    scrivenerAgentPromptTemplate,
} from "../agents/promptTemplates.js";
import { extractSpecializedData } from "./agentsFunctions.js";
import { getDateTime } from "./functions.js";

export const transcribeText = async (req, res, next) => {
    try {
        const prompt = await scrivenerAgentPromptTemplate.invoke({
            text: req.body.texto_informal,
        });

        console.log("Transcribing text...");
        req.body.texto_formalizado = await scrivenerAgent.invoke(prompt);
        console.log("Done transcribing text.");
        next();
    } catch (error) {
        console.error("Error while transcribing text:", error);
        res.status(500).send(error);
    }
};

export const extractGenericData = async (req, res, next) => {
    try {
        const prompt = await extractorAgentPromptTemplate.invoke({
            text: req.body.texto_formalizado,
        });

        console.log("Extracting generic data...");
        const genericJson = await genericDataExtractionAgent.invoke(prompt);

        req.body.genericJson = genericJson;
        console.log("Done extracting generic data.");
        next();
    } catch (error) {
        console.error("Error while extracting generic data:", error);
        res.status(500).send(error);
    }
};

export const callSpecializedAgents = async (req, res) => {
    try {
        let ocurranceJson = req.body.genericJson;
        const crimeTypes = ocurranceJson.tipos_crimes;
        const text = req.body.texto_formalizado;

        console.log("Extracting specialized data...");
        ocurranceJson.dados_crimes = await extractSpecializedData(
            text,
            crimeTypes
        );
        const dateTime = getDateTime();
        ocurranceJson.dados_data_hora.data_registro_ocorrencia = dateTime.date;
        ocurranceJson.dados_data_hora.horario_registro_ocorrencia =
            dateTime.time;
        ocurranceJson.texto_narrativa = text;

        console.log("Done extracting specialized data.");
        res.status(200).json(ocurranceJson);
    } catch (error) {
        console.error("Error while calling calling specialized agents", error);
        res.status(500).send(error);
    }
};
