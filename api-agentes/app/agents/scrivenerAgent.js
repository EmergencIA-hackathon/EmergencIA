import z from "zod";
import { chatGPTModel } from "./baseLLM.js";

const formalizedText = z.object({
    text: z
        .string()
        .describe(
            `Texto reescrito em norma culta. Não faça com que o sentido das palavras seja alterado, apenas corriga os erros ortográficos.`
        ),
});

export const scrivenerAgent = chatGPTModel.withStructuredOutput(formalizedText);
