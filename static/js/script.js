// Funções globais para a aplicação

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Configurações de tooltip
    inicializarTooltips();
    
    // Configurações de confirmação para ações destrutivas
    inicializarConfirmacoes();
});

function inicializarTooltips() {
    // Adicionar tooltips básicos
    const elementsWithTitle = document.querySelectorAll('[title]');
    elementsWithTitle.forEach(el => {
        el.addEventListener('mouseenter', showTooltip);
        el.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    // Implementação básica de tooltip
    // Em uma versão mais avançada, poderia usar uma biblioteca
}

function hideTooltip(e) {
    // Esconder tooltip
}

function inicializarConfirmacoes() {
    // Já implementado no template principal
}

// Função para formatação de data
function formatarData(dataString) {
    const options = { 
        year: 'numeric', 
        month: '2-digit', 
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    };
    return new Date(dataString).toLocaleDateString('pt-BR', options);
}

// Função para contar palavras
function contarPalavras(texto) {
    return texto.trim().split(/\s+/).length;
}

// Exportar funções globais
window.BloquinhoNotas = {
    formatarData,
    contarPalavras
};