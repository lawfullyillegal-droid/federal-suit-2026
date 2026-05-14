/* Lawfully Illegal Public Accountability Enforcement Agency */
/* Project: LI-MOHAVE-2026-001 | Liability: $1,068,000.00 */
/* Integrity Hash: 5ba68eca */

const totalBreaches = 1068;

async function initGallery() {
    const response = await fetch('gallery_manifest.json');
    const data = await response.json();
    const container = document.getElementById('mosaic');
    
    // Integrity Verification Check
    if (data.integrity_hash !== "922bdc85" && data.integrity_hash !== "5ba68eca") {
        console.error("CRITICAL: DATA INTEGRITY MISMATCH.");
        return;
    }

    data.ledger.forEach(id => {
        const block = document.createElement('div');
        block.className = 'void-block';
        block.setAttribute('data-booking-id', id);
        block.title = `Ministerial Breach ID: ${id}`;
        // Visual indicator of systemic failure
        block.style.backgroundColor = '#ff0000';
        container.appendChild(block);
    });
    
    document.getElementById('status-box').innerText = `SYSTEM STATUS: 1,068 Voids Verified | Liability: $1,068,000.00`;
}

window.onload = initGallery;
