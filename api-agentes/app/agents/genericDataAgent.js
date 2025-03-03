import z from "zod";
import { chatGPTModel } from "./baseLLM.js";

// Agente de extração de dados genéricos

const victimData = z.object({
    nome: z.nullable(z.string()).describe("Nome da vítima do delito."),
    documento_identificacao: z
        .nullable(z.string())
        .describe(
            "Documento de identificação da vítima (Quaiser documentos que possam ser usados como identificação pessoal no Brasil)"
        ),
    idade: z.nullable(z.string()).describe("Idade da vítima do delito."),
    data_nascimento: z
        .nullable(z.string())
        .describe("Data de nascimento da vítima."),
    email_contato: z
        .nullable(z.string())
        .describe("Email de contato da vítima."),
    tel_contato: z
        .nullable(z.string())
        .describe("Telefone de contato da vítima."),
});

const offenderData = z.object({
    nome: z.nullable(z.string()).describe("Nome de quem cometeu o delito."),
    idade: z.nullable(z.number()).describe("Idade de que cometeu o delito."),
    data_nascimento: z
        .nullable(z.string())
        .describe("Data de nascimento de que cometeu o delito."),
    caracteristicas_fisicas: z
        .nullable(z.string())
        .describe("Características físicas de quem cometeu o delito."),
    sexo: z.nullable(z.string()).describe("Sexo de quem cometeu o delito."),
    documento_identificacao: z
        .nullable(z.string())
        .describe(
            "Documento de identificação de quem cometeu o delito. (Quaiser documentos que possam ser usados como identificação pessoal no Brasil)"
        ),
    envolvimento: z
        .nullable(z.string())
        .describe(
            "Envolvimento da pessoa na occorrência. Acrescente sempre um \"suposto(a)\" antes do envolvimento. Pois de acordo com o codigo penal brasileiro ngm pode ser declarado culpado antes de sentenca transitada em julgado."
        ),
    condicao_envolvido: z
        .nullable(z.string())
        .describe("Condição física do envolvido."),
});

const eyewitnessData = z.object({
    nome: z.nullable(z.string()).describe("Nome da testemunha."),
    documento_identificacao: z
        .nullable(z.string())
        .describe(
            "Documento de identificação da testemunha. (Quaiser documentos que possam ser usados como identificação pessoal no Brasil)"
        ),
    email_contato: z
        .nullable(z.string())
        .describe("Email de contato da testemunha."),
    tel_contato: z
        .nullable(z.string())
        .describe("Telefone de contato da testemunha."),
    relato: z
        .nullable(z.string())
        .describe("Relato da testemunha sobre a ocorrência, se houver."),
    vinculo_vitima: z
        .nullable(z.string())
        .describe("Vinculo que a testemunha possui com a vítima."),
    vinculo_envolvidos: z.array(
        z
            .nullable(z.string())
            .describe("Vinculo que a testemunha possui com a vítima.")
    ),
});

const crimesCommited = z
    .nullable(z.string())
    .describe(
        "Qual foi o tipo de crime efetuado na ocorrência? Retorne a resposta como estão dentro de cada um dos parenteses: A vítima foi roubada? (Roubo). A vítima sofreu algum tipo de lesão corporal? (Lesão Corporal). A vítima sofreu estelionato? (Estelionato). A denuncia é de tráfico de drogas? (Tráfico de Drogas) A vitima foi alvo de violencia contra a mulher? (Violência Contra Mulher)"
    );

const locationData = z.object({
    tipo_local: z
        .nullable(z.string())
        .describe(
            "Tipo de localização, se foi em via pública, rodovia estadual, etc."
        ),
    nome_municipio: z
        .nullable(z.string())
        .describe("Nome do munícipio em que aconteceu a ocorrência."),
    sigla_uf: z
        .nullable(z.string())
        .describe("Sigla da unidade federal em que aconteceu a ocorrência."),
    endereco_logradouro: z
        .nullable(z.string())
        .describe("Nome logradouro em que aconteceu a ocorrência."),
    endereco_numero: z
        .nullable(z.number())
        .describe("Número do endereço em que aconteceu a ocorrência."),
    endereco_bairro: z
        .nullable(z.string())
        .describe("Nome do bairro em que aconteceu a ocorrência."),
    endereco_complemento: z
        .nullable(z.string())
        .describe("Complemento do endereço em que aconteceu a ocorrência."),
    endereco_ponto_referencia: z
        .nullable(z.string())
        .describe(
            "Ponto de referência para o local em que aconteceu a ocorrência."
        ),
    nome_rodovia: z
        .nullable(z.string())
        .describe("Nome da rodovia em que aconteceu a ocorrência."),
    numero_km: z.nullable(z.number()).describe("Número do quilometro."),
    texto_trecho: z
        .nullable(z.string())
        .describe("Trecho em que aconteceu a ocorrência."), // ??? Mudar isso o quanto antes.
    longitude: z
        .nullable(z.string())
        .describe("longitude de onde aconteceu a ocorrência"), // Recebe do bot
    latitude: z
        .nullable(z.string())
        .describe("latitude de onde aconteceu a ocorrência"), // Recebe do bot
});

const dateTimeData = z.object({
    data_registro_ocorrencia: z.null(), // Isso vem do objeto Date.
    horario_registro_ocorrencia: z.null(), // Isso vem do objeto Date.
    data_acontecimento_ocorrencia: z
        .nullable(z.string())
        .describe("Data em que aconteceu a ocorrência no formato dd/mm/aaaa."),
    horario_acontecimento_ocorrencia: z
        .nullable(z.string())
        .describe("Horário em que aconteceu a ocorrência no formato hh:mm:ss"),
});

// Esse é o formato do JSON que o agente de extração de dados genéricos vai usar.
// Também serve como a base do JSON da ocorrência, que é a junção dos JSONs
// especializados com o JSON genérico.

const genericDataSchema = z.object({
    dados_localizacao: z.nullable(locationData),
    dados_data_hora: dateTimeData,
    dados_vitima: z.nullable(victimData),
    dados_testemunhas: z.nullable(z.array(eyewitnessData)),
    dados_envolvidos: z.nullable(z.array(offenderData)),
    tipos_crimes: z.nullable(z.array(crimesCommited)),
    dados_crimes: z.null(),
    texto_narrativa: z.null(), // Recebe do agente escrivão (?)
    observacao: z.null(), // De onde isso vem?
});

export const genericDataExtractionAgent =
    chatGPTModel.withStructuredOutput(genericDataSchema);
