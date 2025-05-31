 // For autosubmit form
  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('filter-form');
    const inputs = form.querySelectorAll('input, select');

    inputs.forEach(el => {
      el.addEventListener('change', () => {
        if (el.value.trim() !== '') {
          form.submit();
        }
      });
    });
  });
  // Called by button X
  function resetTypeFilter() {
    const url = new URL(window.location);
    url.searchParams.delete('transaction_type');
    window.location.href = url.toString();
  }

  function resetDateFilter() {
    const url = new URL(window.location);
    url.searchParams.delete('start_date');
    url.searchParams.delete('end_date');
    window.location.href = url.toString();
  }
  // Clean empty parameters from URL
  function cleanUrl() {
    const url = new URL(window.location);
    const params = url.searchParams;
    
    for (let [key, value] of [...params.entries()]) {
        if (value === '' || value === null) {
            params.delete(key);
        }
    }
    
    window.history.replaceState({}, '', url.toString());
  }

  document.addEventListener('DOMContentLoaded', cleanUrl);