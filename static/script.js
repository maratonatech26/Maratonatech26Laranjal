let inputPrompt = document.getElementById('inputPrompt');
let inputImage = document.getElementById('inputImage');
let printText = document.getElementById('respostaApiText');

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
    const response = await fetch('http:// localhost/analisar', {
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
