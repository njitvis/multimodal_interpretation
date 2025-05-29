import React, { useState } from 'react';
import Controller from './Controller';
import Source from './Source';
import ClaimEvidenceSection from './ClaimEvidenceSection';

const blankPage = { chartSrc: '', caption: '', context: '', claims: [] };

export default function ChartClaimEditor() {
  const [pages, setPages] = useState([blankPage]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const currentPage = pages[currentIndex];

  const updateCurrentPage = updatedFields => {
    const newPages = [...pages];
    newPages[currentIndex] = { ...newPages[currentIndex], ...updatedFields };
    setPages(newPages);
  };

  const addClaim = () => {
    const newClaims = [
      ...currentPage.claims,
      { claim: '', strategy: '', evidences: [''] }
    ];
    updateCurrentPage({ claims: newClaims });
  };

  const updateClaim = (idx, field, value) => {
    const newClaims = currentPage.claims.map((c, i) =>
      i === idx ? { ...c, [field]: value } : c
    );
    updateCurrentPage({ claims: newClaims });
  };

  const updateClaimOrder = (newClaims) => {
    updateCurrentPage({ claims: newClaims });
  };

  const deleteClaim = idx => {
    const newClaims = currentPage.claims.filter((_, i) => i !== idx);
    updateCurrentPage({ claims: newClaims });
  };

  const addEvidence = idx => {
    const newEvidences = [...currentPage.claims[idx].evidences, ''];
    const newClaims = currentPage.claims.map((c, i) =>
      i === idx ? { ...c, evidences: newEvidences } : c
    );
    updateCurrentPage({ claims: newClaims });
  };

  const updateEvidence = (claimIdx, evIdx, value) => {
    const newClaims = currentPage.claims.map((c, i) => {
      if (i === claimIdx) {
        const evs = c.evidences.map((e, j) => (j === evIdx ? value : e));
        return { ...c, evidences: evs };
      }
      return c;
    });
    updateCurrentPage({ claims: newClaims });
  };

  const deleteEvidence = (claimIdx, evIdx) => {
    const newClaims = currentPage.claims.map((c, i) => {
      if (i === claimIdx) {
        const evs = c.evidences.filter((_, j) => j !== evIdx);
        return { ...c, evidences: evs.length ? evs : [''] };
      }
      return c;
    });
    updateCurrentPage({ claims: newClaims });
  };

  const savePage = () => {
    const blob = new Blob([JSON.stringify(pages, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'annotated_claims.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  const nextPage = () => {
    if (currentIndex < pages.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      setPages([...pages, blankPage]);
      setCurrentIndex(pages.length);
    }
  }

  const loadFromFile = e => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = evt => {
      try {
        console.log("loading");
        const data = JSON.parse(evt.target.result);
        if (Array.isArray(data)) {
          setPages(data);
          setCurrentIndex(0);
        } else {
          alert('Invalid JSON format.');
        }
        console.log("loaded");
      } catch {
        alert('Error parsing JSON file.');
      }
    };
    reader.readAsText(file);
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex flex-1">
        <Source currentPage={currentPage} updateCurrentPage={updateCurrentPage} loadFromFile={loadFromFile} />

        <ClaimEvidenceSection 
        currentPage={currentPage}
        addClaim={addClaim} updateClaim={updateClaim} deleteClaim={deleteClaim} updateClaimOrder={updateClaimOrder}
        addEvidence={addEvidence} updateEvidence={updateEvidence} deleteEvidence={deleteEvidence} />
      </div>

      <Controller setCurrentIndex={setCurrentIndex} nextPage={nextPage} savePage={savePage} />
    </div>
  );
}
