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

// <form data-persist="unique-key">: keeps what was typed so a refresh (or a closed tab)
// doesn't lose it. The draft is dropped once the form is submitted.
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('form[data-persist]').forEach((form) => {
        const key = `draft:${form.dataset.persist}`;
        const fields = [...form.querySelectorAll('input:not([type="hidden"])')];

        const read = () => {
            try {
                return JSON.parse(window.localStorage.getItem(key)) || [];
            } catch (_) {
                return [];
            }
        };

        const saved = read();
        fields.forEach((field, i) => {
            if (saved[i] != null) field.value = saved[i];
        });

        // Continue where the user left off.
        const firstEmpty = fields.find((field) => field.value === '');
        if (firstEmpty) firstEmpty.focus();

        form.addEventListener('input', () => {
            try {
                window.localStorage.setItem(key, JSON.stringify(fields.map((field) => field.value)));
            } catch (_) { /* storage unavailable: the form still works, it just won't be kept */ }
        });

        form.addEventListener('submit', () => {
            try {
                window.localStorage.removeItem(key);
            } catch (_) {}
        });
    });
});
