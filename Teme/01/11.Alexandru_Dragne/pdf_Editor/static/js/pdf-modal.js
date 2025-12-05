// PDF Preview Modal with PDF.js
class PDFPreviewModal {
    constructor() {
        this.modal = null;
        this.pdfDoc = null;
        this.pageNum = 1;
        this.scale = 1.5;
        this.canvas = null;
        this.ctx = null;
        this.pageRendering = false;
        this.pageNumPending = null;
        
        this.init();
    }
    
    init() {
        // Create modal HTML
        const modalHTML = `
            <div id="pdf-preview-modal" class="pdf-modal">
                <div class="pdf-modal-content">
                    <div class="pdf-modal-header">
                        <h3>📄 PDF Preview</h3>
                        <button class="pdf-modal-close" onclick="pdfModal.close()">&times;</button>
                    </div>
                    <div class="pdf-modal-body">
                        <div class="pdf-canvas-wrapper">
                            <canvas id="modal-pdf-canvas"></canvas>
                        </div>
                        <div class="pdf-modal-controls">
                            <button id="modal-prev-page" class="icon-btn">← Previous</button>
                            <span class="page-info">
                                Page <span id="modal-page-num"></span> of <span id="modal-page-count"></span>
                            </span>
                            <button id="modal-next-page" class="icon-btn">Next →</button>
                            
                            <div class="zoom-controls">
                                <button id="modal-zoom-out" class="icon-btn">−</button>
                                <span class="page-info"><span id="modal-zoom-level">100</span>%</span>
                                <button id="modal-zoom-in" class="icon-btn">+</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Append to body
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        this.modal = document.getElementById('pdf-preview-modal');
        this.canvas = document.getElementById('modal-pdf-canvas');
        this.ctx = this.canvas.getContext('2d');
        
        // Event listeners
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Close modal on background click
        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });
        
        // Navigation buttons
        document.getElementById('modal-prev-page').addEventListener('click', () => {
            if (this.pageNum <= 1) return;
            this.pageNum--;
            this.queueRenderPage(this.pageNum);
        });
        
        document.getElementById('modal-next-page').addEventListener('click', () => {
            if (this.pageNum >= this.pdfDoc.numPages) return;
            this.pageNum++;
            this.queueRenderPage(this.pageNum);
        });
        
        // Zoom buttons
        document.getElementById('modal-zoom-in').addEventListener('click', () => {
            this.scale += 0.25;
            document.getElementById('modal-zoom-level').textContent = Math.round(this.scale * 100);
            this.queueRenderPage(this.pageNum);
        });
        
        document.getElementById('modal-zoom-out').addEventListener('click', () => {
            if (this.scale > 0.5) {
                this.scale -= 0.25;
                document.getElementById('modal-zoom-level').textContent = Math.round(this.scale * 100);
                this.queueRenderPage(this.pageNum);
            }
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (!this.modal.classList.contains('active')) return;
            
            if (e.key === 'Escape') this.close();
            if (e.key === 'ArrowLeft') document.getElementById('modal-prev-page').click();
            if (e.key === 'ArrowRight') document.getElementById('modal-next-page').click();
        });
    }
    
    async open(pdfUrl) {
        try {
            // Load PDF
            const loadingTask = pdfjsLib.getDocument(pdfUrl);
            this.pdfDoc = await loadingTask.promise;
            
            // Reset state
            this.pageNum = 1;
            this.scale = 1.5;
            
            // Update UI
            document.getElementById('modal-page-count').textContent = this.pdfDoc.numPages;
            document.getElementById('modal-zoom-level').textContent = Math.round(this.scale * 100);
            
            // Show modal
            this.modal.classList.add('active');
            document.body.style.overflow = 'hidden';
            
            // Render first page
            this.renderPage(this.pageNum);
            
        } catch (error) {
            console.error('Error loading PDF:', error);
            alert('Error loading PDF preview');
        }
    }
    
    close() {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
        
        // Cleanup
        if (this.pdfDoc) {
            this.pdfDoc.destroy();
            this.pdfDoc = null;
        }
    }
    
    renderPage(num) {
        this.pageRendering = true;
        
        this.pdfDoc.getPage(num).then(page => {
            const viewport = page.getViewport({ scale: this.scale });
            this.canvas.height = viewport.height;
            this.canvas.width = viewport.width;

            const renderContext = {
                canvasContext: this.ctx,
                viewport: viewport
            };

            const renderTask = page.render(renderContext);

            renderTask.promise.then(() => {
                this.pageRendering = false;
                if (this.pageNumPending !== null) {
                    this.renderPage(this.pageNumPending);
                    this.pageNumPending = null;
                }
            });
        });

        document.getElementById('modal-page-num').textContent = num;
        this.updateButtons();
    }
    
    queueRenderPage(num) {
        if (this.pageRendering) {
            this.pageNumPending = num;
        } else {
            this.renderPage(num);
        }
    }
    
    updateButtons() {
        document.getElementById('modal-prev-page').disabled = (this.pageNum <= 1);
        document.getElementById('modal-next-page').disabled = (this.pageNum >= this.pdfDoc.numPages);
    }
}

// Initialize modal on page load
let pdfModal;
document.addEventListener('DOMContentLoaded', () => {
    // Load PDF.js
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    script.onload = () => {
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        pdfModal = new PDFPreviewModal();
    };
    document.head.appendChild(script);
});
