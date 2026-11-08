// Shared small behaviours, driven by data-attributes so templates stay declarative.

// data-confirm="message" on a button/link asks before acting.
document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-confirm]');
    if (el && !window.confirm(el.dataset.confirm)) {
        e.preventDefault();
    }
});

// <form data-autosubmit>: submit as soon as a <select> gets a value.
document.addEventListener('change', (e) => {
    const form = e.target.closest('form[data-autosubmit]');
    if (!form || !e.target.matches('select') || !e.target.value) return;

    form.requestSubmit(form.querySelector('button[type="submit"]'));
});

document.addEventListener('DOMContentLoaded', () => {
    // Without JS the buttons stay visible and the form still works.
    document.querySelectorAll('form[data-autosubmit] button[type="submit"]').forEach((b) => {
        b.hidden = true;
    });

    // <form data-enter-next>: Enter jumps to the next field, the last one submits.
    document.querySelectorAll('form[data-enter-next]').forEach((form) => {
        form.addEventListener('keydown', (e) => {
            if (e.key !== 'Enter' || e.target.tagName !== 'INPUT') return;

            const fields = [...form.querySelectorAll('input:not([type="hidden"])')];
            const i = fields.indexOf(e.target);

            if (i > -1 && i < fields.length - 1) {
                e.preventDefault();
                fields[i + 1].focus();
            }
        });
    });
});
