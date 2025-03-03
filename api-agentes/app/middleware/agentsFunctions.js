import {
    batteryAgentPromptTemplate,
    theftAgentPromptTemplate,
    fraudAgentPromptTemplate,
    trafficAgentPromptTemplate,
    extractorViolenceAgentPromptTemplate,
} from "../agents/promptTemplates.js";

import { batteryDataExtractionAgent } from "../agents/specialized/batteryDataAgent.js";
import { theftDataExtractionAgent } from "../agents/specialized/theftDataAgent.js";
import { violenceDataExtractionAgent } from "../agents/specialized/violenceAgainstWomenAgent.js";
import { fraudDataExtractionAgent } from "../agents/specialized/fraudDataAgent.js";;
import { trafficDataExtrationAgent } from "../agents/specialized/trafficDataAgent.js";;

async function extractTrafficData(text) {
    try {
        const prompt = await trafficAgentPromptTemplate.invoke({
            text: text,
        });
        const trafficJson = await trafficDataExtrationAgent.invoke(prompt);

        console.log("Done extracting traffic data.");
        return trafficJson;
    } catch (error) {
        console.error("Error while extracting trafic data:", error);
        return null;
    }
}

async function extractFraudData(text) {
    try {
        const prompt = await fraudAgentPromptTemplate.invoke({
            text: text,
        });
        const fraudJson = await fraudDataExtractionAgent.invoke(prompt);

        console.log("Done extracting fraud data.");
        return fraudJson;
    } catch (error) {
        console.error("Error while extracting fraud data:", error);
        return null;
    }
}

async function extractTheftData(text) {
    try {
        const prompt = await theftAgentPromptTemplate.invoke({
            text: text,
        });

        const theftJson = await theftDataExtractionAgent.invoke(prompt);

        console.log("Done extracting theft data.");
        return theftJson;
    } catch (error) {
        console.error("Error while extracting theft data:", error);
        return null;
    }
}

async function extractBatteryData(text) {
    try {
        const prompt = await batteryAgentPromptTemplate.invoke({
            text: text,
        });

        const batteryJson = await batteryDataExtractionAgent.invoke(prompt);

        console.log("Done extracting battery data.");
        return batteryJson;
    } catch (error) {
        console.error("Error while extracting battery data:", error);
        return null;
    }
}

async function extractViolenceData(text) {
    try {
        // Gera o prompt e faz a extração dos dados
        const prompt = await extractorViolenceAgentPromptTemplate.invoke({
            text,
        });
        const violenceJson = await violenceDataExtractionAgent.invoke(prompt);

        // Garantindo que violenceJson seja um objeto válido
        const extractedViolenceData = {};

        // Verifique se violenceJson é um objeto não nulo
        if (violenceJson && typeof violenceJson === "object") {
            // Processa os tipos de violência
            for (const [violenceType, data] of Object.entries(violenceJson)) {
                if (Array.isArray(data)) {
                    // Filtra apenas os objetos onde pelo menos um campo seja `true`
                    const filteredArray = data.filter((obj) =>
                        Object.values(obj).some((value) => value === true)
                    );

                    if (filteredArray.length > 0) {
                        extractedViolenceData[violenceType] = filteredArray;
                    }
                } else if (typeof data === "object" && data !== null) {
                    // Trata o caso específico do feminicídio, que é um único objeto e não um array
                    const filteredData = Object.fromEntries(
                        Object.entries(data).filter(
                            ([_, value]) => value === true
                        )
                    );

                    if (Object.keys(filteredData).length > 0) {
                        extractedViolenceData[violenceType] = filteredData;
                    }
                }
            }
        }

        // Se algum dado foi extraído, retorna o objeto estruturado
        if (Object.keys(extractedViolenceData).length > 0) {
            return { "Violência contra a mulher": extractedViolenceData };
        }

        // Se não houver dados extraídos, retorna um objeto vazio
        return { "Violência contra a mulher": {} };
    } catch (error) {
        console.error("Erro ao extrair dados de violência:", error);
        return { "Violência contra a mulher": {} }; // Retorna um objeto vazio em caso de erro
    }
}

export async function extractSpecializedData(text, crimesArray) {
    const crimesMap = new Map();
    crimesMap.set("Roubo", extractTheftData);
    crimesMap.set("Lesão Corporal", extractBatteryData);
    crimesMap.set("Estelionato", extractFraudData);
    crimesMap.set("Tráfico de Drogas", extractTrafficData);
    crimesMap.set("Violência Contra Mulher", extractViolenceData);

    if (crimesArray === null) {
        return null
    }

    let specializedJsonArr = crimesArray.map(async (crimeType) => {
        if (crimesMap.has(crimeType)) {
            return await crimesMap.get(crimeType)(text);
        }
        return null
    })

    specializedJsonArr = Promise.all(specializedJsonArr)

    return specializedJsonArr;
}
