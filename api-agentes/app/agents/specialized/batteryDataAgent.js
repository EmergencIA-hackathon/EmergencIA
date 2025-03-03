import z from "zod";
import { chatGPTModel } from "../baseLLM.js";

const mildBodilyInjuryData = z.object({
    tipo: z.literal("leve"),
    arranhoes: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui arranhões graças ao acontecido na ocorrência?"
        ),
    hematomas: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui hematomas graças ao acontecido na ocorrência?"
        ),
    pequenos_cortes: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui pequenos cortes graças ao acontecido na ocorrência?"
        ),
});

const seriousBodilyInjuryData = z.object({
    tipo: z.literal("grave"),
    trauma_osseo: z
        .nullable(z.boolean())
        .describe(
            "A vítima sofreu algum tipo de lesão óssea, podendo ser uma fratura, contusão, luxação ou torção."
        ),
    incapacidade_ocupacoes_habituais: z
        .nullable(z.boolean())
        .describe(
            "A vítima está incapacitada para realização de ocupações habituais graças ao acontecido na ocorrência?"
        ),
    perigo_vida: z
        .nullable(z.boolean())
        .describe(
            "A vítima correu ou corre perigo de vida graças ao acontecido na ocorrência?"
        ),
    debilidade_permanente: z
        .nullable(z.boolean())
        .describe(
            "A vítima sofreu debilitação permanente de algum membro, sentido ou função graças ao acontecido na ocorrência?"
        ),
    aceleracao_parto: z
        .nullable(z.boolean())
        .describe(
            "A vítima sofreu aceleração no parto graças ao acontecido na ocorrência?"
        ),
});

const severeBodilyInjuryData = z.object({
    tipo: z.literal("gravissima"),
    incapacidade_permanete_trabalho: z
        .nullable(z.boolean())
        .describe(
            "A vítima está incapacitada de trabalhar permanentemente graças ao acontecido na ocorrência?"
        ),
    efermidade_incuravel: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui efermidade incuravel graças ao acontecido na ocorrência?"
        ),
    perda_permanente: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui perda o inutilização permanente de algum membro, sentido ou função graças ao acontecido na ocorrência?"
        ),
    deformidade_permanente: z
        .nullable(z.boolean())
        .describe(
            "A vítima possui deformidade permanente graças ao acontecido na ocorrência?"
        ),
    aborto: z
        .nullable(z.boolean())
        .describe("A vítima sofreu aborto graças ao acontecido na ocorrência?"),
});

const bodilyInjuryFollowedByDeathData = z.object({
    tipo: z.literal("Lesão seguida de morte"),
    lesao_seguida_morte: z
        .nullable(z.boolean())
        .describe(
            "A lesão corporal resultou na morte da vítima e as circunstâncias evidenciam que o envolvido não quís o resultado, nem assumiu o risco de produzí-lo"
        ),
});

const unintentionalBodilyInjuryData = z.object({
    tipo: z.literal("Lesão culposa"),
    lesao_culposa: z
        .nullable(z.boolean())
        .describe(
            "O envolvido não teve a intenção de causar lesões corporais na vítima. (Lesão corporal culposa)"
        ),
});

const domesticViolenceData = z.object({
    tipo: z.literal("Violência doméstica"),
    violencia_domestica: z
        .nullable(z.boolean())
        .describe(
            "A lesão corporal foi praticada contra algum membro da fámilia (irmãos, pais, filhos, cônjuge ou companheiro) ou com quem conviva ou tenha convivido? (Violência doméstica)"
        ),
});

const batteryDataSchema = z.object({
    tipo_crime: z.literal("Lesão corporal"),
    dados_lesao_corporal_leve: z.nullable(mildBodilyInjuryData),
    dados_lesao_corporal_grave: z.nullable(seriousBodilyInjuryData),
    dados_lesao_corporal_gravissima: z.nullable(severeBodilyInjuryData),
    dados_lesao_corporal_seguida_morte: z.nullable(
        bodilyInjuryFollowedByDeathData
    ),
    dados_lesao_corporal_culposa: z.nullable(unintentionalBodilyInjuryData),
    dados_violencia_domestica: z.nullable(domesticViolenceData),
});

export const batteryDataExtractionAgent =
    chatGPTModel.withStructuredOutput(batteryDataSchema);
