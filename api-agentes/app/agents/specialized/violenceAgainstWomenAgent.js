import z from "zod";
import { chatGPTModel } from "../baseLLM.js";

// Agente de extração de dados de violência contra a mulher

const violenciaFisicaData = z.object({
    agressao_fisica: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve espancamento, lesões, ferimentos e/ou outras formas de tortura."
        ),
    arremesso_objetos: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve arremesso de objetos na intenção de machucar."
        ),
    sacudir: z
        .nullable(z.boolean())
        .describe("Indica se a vítima foi sacudida."),
    aperto_bracos: z
        .nullable(z.boolean())
        .describe("Indica se a vítima foi segurada com força."),
});

const violenciaMoralData = z.object({
    acusacoes: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve acusações caluniosas e críticas mentirosas sobre traição e/ou a índole/conduta da vítima."
        ),
    exposicao: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve exposição da vida íntima do casal e/ou da vítima como fotos, falas desnecessárias, etc."
        ),
});

const violenciaPsicologicaData = z.object({
    constrangimento: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve a desvalorização moral, diminuição da autoestima e/ou deboche público da vítima."
        ),
    opressao: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve um comportamento e/ou controle obsessivo sobre a vítima."
        ),
    ameacas: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve xingamentos e/ou ameaças direcionados à vítima."
        ),
    humilhacao: z
        .nullable(z.boolean())
        .describe("Indica se houve humilhação da vítima."),
    restricao: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve restrição de ação, decisão e/ou crença sobre a vítima."
        ),
    gaslighting: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve distorção de fatos, omissão de situações ou quaisquer formas de impor dúvida à vítima sobre sua memória e sanidade mental."
        ),
});

const violenciaSexualData = z.object({
    estupro_assedio: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve uma imposição e/ou obrigação à vítima de atos sexuais, sejam eles sexo à força ou a realização de fetiches próprios que causem desconforto/repulsa."
        ),
    impedimento: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve impedimento à vítima de utilizar métodos contraceptivos e/ou obrigação da realização de abortos."
        ),
});

const violenciaPatrimonialData = z.object({
    controle_financeiro: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve um controle, retirada e/ou extorsão do dinheiro da vítima."
        ),
    privacao: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve a retenção de documentos pessoais da vítima e/ou a destruição dos mesmos, a privatização de bens e/ou estelionato."
        ),
    danos_patrimoniais: z
        .nullable(z.boolean())
        .describe(
            "Indica se houve danos de propósito a objetos pertencentes à vítima ou dos quais fossem de seu gosto."
        ),
});

const feminicidioData = z.object({
    violencia_de_genero: z
        .nullable(z.boolean())
        .describe(
            "Indica se a vítima veio a óbito em razão de pertencer ao gênero feminino."
        ),
});

const violenceDataSchema = z.object({
    violencia_fisica: z.nullable(z.array(violenciaFisicaData)),
    violencia_moral: z.nullable(z.array(violenciaMoralData)),
    violencia_psicologica: z.nullable(z.array(violenciaPsicologicaData)),
    violencia_sexual: z.nullable(z.array(violenciaSexualData)),
    violencia_patrimonial: z.nullable(z.array(violenciaPatrimonialData)),
    feminicidio: z.nullable(feminicidioData),
});

export const violenceDataExtractionAgent =
    chatGPTModel.withStructuredOutput(violenceDataSchema);

