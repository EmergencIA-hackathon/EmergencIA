import z from "zod";
import { chatGPTModel } from "../baseLLM.js";

const victimBankData = z.object({
    nomeBanco: z.nullable(z.string()).describe(`Nome do banco da vitima.`),
    conta: z.nullable(z.string()).describe(`Numero da conta da vitima.`),
    agencia: z
        .nullable(z.string())
        .describe(`Numero da agencia bancaria da vitima`),
    valor: z
        .nullable(z.string())
        .describe(
            `Valor subtraido da conta da vitima ou pago em caso de golpes de compra e venda`
        ),
});

const offenderBankData = z.object({
    nomeBanco: z
        .nullable(z.string())
        .describe(`Nome do banco da estelionatario.`),
    conta: z
        .nullable(z.string())
        .describe(`Numero da conta da estelionatario.`),
    agencia: z
        .nullable(z.string())
        .describe(`Numero da agencia bancaria da estelionatario`),
    chavePix: z.nullable(z.string()).describe(`Chave pix do estelionatario`),
});

const victimCreditCard = z.object({
    bandeira: z
        .nullable(z.string())
        .describe(`Bandeira do cartao de credito da vitima.`),
    numero: z
        .nullable(z.string())
        .describe(`Numero do cartao de credito da vitima.`),
    validade: z
        .nullable(z.string())
        .describe(`Validade do cartao de credito da vitima`),
    codigoSeguranca: z
        .nullable(z.string())
        .describe(`Codigo de seguranca do cartao de credito da vitima`),
});

const siteInfos = z.object({
    endereco: z
        .nullable(z.string())
        .describe(`Endereco do site usado no golpe.`),
    conta: z
        .nullable(z.string())
        .describe(
            `Conta que aplicou o golpe da vitima, exemplo @ do instagran ou tiktok.`
        ),
});

const documentData = z.object({
    tipo: z
        .nullable(z.string())
        .describe(
            `Tipo do documento falsificado, como por exemplo rg, cnh, passaporte ou outro.`
        ),
    numero: z.nullable(z.string()).describe(`Numero do documento falsificado.`),
});

const productData = z.object({
    nome: z.nullable(z.string()).describe(`Nome do objeto falso vendido.`),
    descricao: z
        .nullable(z.string())
        .describe(`Descricao do objeto falsa vendido.`),
    marca: z.nullable(z.string()).describe(`Marca do objeto falso vendido.`),
});

const contractData = z.object({
    tipo: z
        .nullable(z.string())
        .describe(
            `Tipo do falso contrato, por exemplo contrato de formatura, contrato de prestacao de algum servico, contrato de aluguel, entre outros.`
        ),
    descricao: z
        .nullable(z.string())
        .describe(`Descricao resumida do contrato.`),
    data: z
        .nullable(z.string())
        .describe(`Data de assinatura do contrato falso.`),
    nomeEmpresa: z
        .nullable(z.string())
        .describe(`Nome da empresa ou pessoa contratada.`),
    cnpj_cpf: z
        .nullable(z.string())
        .describe(`CNPJ da empresa ou CPF da pessoa contratada.`),
});

const fraudDataSchema = z.object({
    dados_bancarios_vitima: z.nullable(z.array(victimBankData)),
    dados_bancarios_acusado: z.nullable(z.array(offenderBankData)),
    dados_cartao_vitima: z.nullable(z.array(victimCreditCard)),
    informacoes_sites: z.nullable(z.array(siteInfos)),
    documentos_falsificados: z.nullable(z.array(documentData)),
    produtos_falsos_vendidos: z.nullable(z.array(productData)),
    dados_contratos: z.nullable(z.array(contractData)),
});

export const fraudDataExtractionAgent =
    chatGPTModel.withStructuredOutput(fraudDataSchema);
