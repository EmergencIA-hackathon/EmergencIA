import z from "zod";
import { chatGPTModel } from "../baseLLM.js";

const vehicleData = z.object({
    marca: z.nullable(z.string()).describe(`Marca do veiculo roubado.`),
    modelo: z.nullable(z.string()).describe(`Modelo do veiculo roubado`),
    cor: z.nullable(z.string()).describe(`Cor do veiculo roubado`),
    ano: z.nullable(z.string()).describe(`Ano do veiculo roubado`),
    placa: z.nullable(z.string()).describe(`Placa do veiculo roubado`),
    renavam: z.nullable(z.string()).describe(`Renavan do veiculo roubado`),
});

const celphoneData = z.object({
    marca: z.nullable(z.string()).describe(`Marca do celular roubado.`),
    modelo: z.nullable(z.string()).describe(`Modelo do celular roubado`),
    cor: z.nullable(z.string()).describe(`Cor do celular roubado`),
});

const documentData = z.object({
    tipo: z
        .nullable(z.string())
        .describe(
            `Tipo do documento roubado, como por exemplo rg, cnh, passaporte ou outro.`
        ),
    numero: z.nullable(z.string()).describe(`Numero do documento roubado.`),
});

const objectData = z.object({
    nome: z.nullable(z.string()).describe(`Nome do objeto roubado.`),
    descricao: z.nullable(z.string()).describe(`Descricao do objeto roubado.`),
    marca: z.nullable(z.string()).describe(`Marca do objeto roubado.`),
});

const informationData = z.object({
    usoDeArma: z.nullable(z.boolean()).describe(`Houve uso de arma?`),
    usoDeViolencia: z.nullable(z.boolean()).describe(`Houve uso de violencia?`),
});

const theftDataSchema = z.object({
    dados_veiculos: z.nullable(z.array(vehicleData)),
    dados_celulares: z.nullable(z.array(celphoneData)),
    dados_documentos: z.nullable(z.array(documentData)),
    dados_objetos: z.nullable(z.array(objectData)),
    dados_complementares: z.nullable(informationData),
});

export const theftDataExtractionAgent =
    chatGPTModel.withStructuredOutput(theftDataSchema);
