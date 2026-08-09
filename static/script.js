let inputPrompt = document.getElementById('inputPrompt');
let inputImage = document.getElementById('inputImage');
let printText = document.getElementById('respostaApiText');
const promptPhishing = 
  "Atue como um especialista em cibersegurança. Explique o conceito de Phishing, " +
  "quais são os tipos mais comuns (email, sites falsos) e forneça 3 dicas práticas " +
  "de como identificar e se proteger contra esse tipo de ataque. Mas, seja o mais breve possível e pergunte se ha alguma dúvida";

const promptDeepfakes = 
  "Atue como um especialista em inteligência artificial e segurança digital. Explique o que são Deepfakes, " +
  "como essa tecnologia é usada para golpes e quais sinais visuais ou auditivos ajudam a identificar um conteúdo manipulado. Mas, seja o mais breve possível e pergunte se ha alguma dúvida";

const promptSmishing = 
  "Atue como um analista de segurança da informação. Explique o que é Smishing (Phishing via SMS ou aplicativos de mensagem), " +
  "dê exemplos de abordagens comuns usadas por criminosos e ensine como reagir ao receber uma mensagem suspeita. Mas, seja o mais breve possível e pergunte se ha alguma dúvida";

const promptEngenhariaSocial = 
  "Atue como um auditor de segurança. Explique o conceito amplo de Engenharia Social no contexto da cibersegurança, " +
  "quais são os gatilhos psicológicos mais explorados (urgência, autoridade, medo) e como criar uma cultura de prevenção. Mas, seja o mais breve possível e pergunte se ha alguma dúvida";

const promptEngajamento = 
  "Atue como um educador em tecnologia. Elabore um quiz rápido e interativo com 3 perguntas de múltipla escolha sobre segurança digital " +
  "para testar e engajar o usuário. Inclua o gabarito ao final com explicações breves. Mas, seja o mais breve possível e pergunte se ha alguma dúvida";

// Função genérica que junta o prompt base com o texto opcional do usuário
function montarPayload(promptBase) {
  const inputUsuario = document.getElementById('inputPrompt') 
    ? document.getElementById('inputPrompt').value.trim() 
    : '';

  // Se o usuário digitou algo, concatena com o prompt base
  if (inputUsuario) {
    return `${promptBase}\n\nO usuário também enviou a seguinte dúvida complementar: "${inputUsuario}"`;
  }

  return promptBase;
}

// Funções associadas a cada botão do seu HTML/interface
async function tratarPhishing() {
  const textoFinal = montarPayload(promptPhishing);
  await enviarFormularioAutomatico(textoFinal);
}

async function tratarDeepfakes() {
  const textoFinal = montarPayload(promptDeepfakes);
  await enviarFormularioAutomatico(textoFinal);
}

async function tratarSmishing() {
  const textoFinal = montarPayload(promptSmishing);
  await enviarFormularioAutomatico(textoFinal);
}

async function tratarEngenhariaSocial() {
  const textoFinal = montarPayload(promptEngenhariaSocial);
  await enviarFormularioAutomatico(textoFinal);
}

async function tratarEngajamento() {
  const textoFinal = montarPayload(promptEngajamento);
  await enviarFormularioAutomatico(textoFinal);
}

async function enviarFormularioAutomatico(textoPrompt) {
  const printText = document.getElementById('respostaApiText');
  printText.innerHTML = `<h1 class="resposta">PROCESSANDO SUA BUSCA...</h1>`;

  const formData = new FormData();
  formData.append('texto', textoPrompt);

  // Se houver arquivo de imagem selecionado no input, anexa junto
  const inputImage = document.getElementById('inputImage');
  if (inputImage && inputImage.files[0]) {
    formData.append('imagem', inputImage.files[0]);
  }

  try {
    const response = await fetch('/analisar', {
      method: 'POST',
      body: formData
    });

    const resultado = await response.json();

    if (resultado.sucesso) {
      printText.innerHTML = `<div class="resposta">${resultado.analise}</div>`;
    } else {
      const detalheErro = typeof resultado.erro === 'object' 
        ? JSON.stringify(resultado.erro) 
        : resultado.erro;
      printText.innerHTML = `<p class="resposta">Erro: ${detalheErro}</p>`;
    }
  } catch (error) {
    printText.innerHTML = `<p class="resposta">Erro de conexão com o servidor: ${error.message}</p>`;
  }
}


async function enviarParaServidor() {
  printText.innerHTML = `<h1 class="resposta">PROCESSANDO SUA BUSCA...</h1>`;

  const texto = inputPrompt.value.trim();
  const arquivo = inputImage.files[0]; // Pode ser undefined se o usuário não escolheu arquivo

  // Validação: Exige apenas o texto
  if (!texto) {
    printText.innerHTML = `<p class="resposta">Por favor, digite um texto!</p>`;
    return;
  }

  const formData = new FormData();
  formData.append('texto', texto);

  // Adiciona a imagem no FormData SOMENTE se ela existir
  if (arquivo) {
    formData.append('imagem', arquivo);
  }

  try {
    const response = await fetch('/analisar', {
      method: 'POST',
      body: formData
    });

    const resultado = await response.json();
    
    if (resultado.sucesso) {
      printText.innerHTML = `<p class="resposta">${resultado.analise}</p>`;
    } else {
      const detalheErro = typeof resultado.erro === 'object' 
        ? JSON.stringify(resultado.erro) 
        : resultado.erro;
      printText.innerHTML = `<p class="resposta">Erro: ${detalheErro}</p>`;
    }
  } catch (error) {
    printText.innerHTML = `<p class="resposta">Erro de conexão com o servidor Flask.</p>`;
  }
}
