import { ChatOpenAI } from "@langchain/openai";

export const chatGPTModel = new ChatOpenAI({
    model: process.env.OPENAI_MODEL,
    apiKey: process.env.OPENAI_API_KEY,
    temperature: 0,
});
