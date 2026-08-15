// Elementos Globais
const inputPrompt = document.getElementById('inputPrompt');
const inputImage = document.getElementById('inputImage');
const printText = document.getElementById('respostaApiText');
const menuVisor = document.getElementById('visor');
const botaoMenu = document.getElementById('menu');

// Função genérica que junta o prompt base com o texto opcional do usuário
function montarPayload(promptBase) {
  const inputUsuario = document.getElementById('inputPrompt') ?
    document.getElementById('inputPrompt').value.trim() :
    '';
  
  if (inputUsuario) {
    return `${promptBase}\n\nO usuário também enviou a seguinte dúvida complementar: "${inputUsuario}"`;
  }
  return promptBase;
}

// Funções associadas a cada botão de tópicos/ameaças
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

// Envio automático para os botões temáticos
async function enviarFormularioAutomatico(textoPrompt) {
  printText.innerHTML = `<h1 class="resposta">PROCESSANDO SUA BUSCA...</h1>`;
  const formData = new FormData();
  formData.append('texto', textoPrompt);
  
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
      const HTMLFormatado = marked.parse(resultado.analise);
      printText.innerHTML = `<div class="resposta-card">${HTMLFormatado}</div>`;
    } else {
      const detalheErro = typeof resultado.erro === 'object' ?
        JSON.stringify(resultado.erro) :
        resultado.erro;
      printText.innerHTML = `<p class="resposta">Erro: ${detalheErro}</p>`;
    }
  } catch (error) {
    printText.innerHTML = `<p class="resposta">Erro de conexão com o servidor: ${error.message}</p>`;
  }
}

// Envio padrão pelo input principal (Mantido da versão estável)
async function enviarParaServidor() {
  printText.innerHTML = `<h1 class="resposta">PROCESSANDO SUA BUSCA...</h1>`;
  const texto = inputPrompt.value.trim();
  const arquivo = inputImage.files[0];
  
  if (!texto) {
    printText.innerHTML = `<p class="resposta">Por favor, digite um texto!</p>`;
    return;
  }
  
  const formData = new FormData();
  formData.append('texto', texto);
  
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
      const HTMLFormatado = marked.parse(resultado.analise);
      printText.innerHTML = `<div class="resposta-card">${HTMLFormatado}</div>`;
    } else {
      const detalheErro = typeof resultado.erro === 'object' ?
        JSON.stringify(resultado.erro) :
        resultado.erro;
      printText.innerHTML = `<p class="resposta">Erro: ${detalheErro}</p>`;
    }
  } catch (error) {
    printText.innerHTML = `<p class="resposta">Erro de conexão com o servidor Flask.</p>`;
  }
}

// Controle do Menu Lateral / Visor
function Menu() {
  menuVisor.classList.toggle('ativo');
  menuVisor.innerHTML = `
        <a href="/videos" class="matrix menuBotao">
            Saiba mais sobre segurança digital 
            <div class="code-rain"></div>
        </a>
        <a href="/noticias" class="matrix menuBotao">
             Últimas notícias do mundo digital *desenvolvimento
            <div class="code-rain"></div>
        </a>
        <a href="/quiz" class="matrix menuBotao">
            Fique atento sobre golpes *desenvolvimento
            <div class="code-rain"></div>
        </a>
    `;
}

// Ouvinte para fechar o menu ao clicar fora dele
window.addEventListener('click', function(event) {
  if (
    menuVisor && menuVisor.classList.contains('ativo') &&
    !menuVisor.contains(event.target) &&
    botaoMenu && !botaoMenu.contains(event.target)
  ) {
    menuVisor.classList.remove('ativo');
  }
});