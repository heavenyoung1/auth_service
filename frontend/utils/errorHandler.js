// Мапа для локализации ошибок
const errorLocalization = {
    "String should have at least 6 characters": "должен содержать минимум 6 символов",
    "String should have at least 4 characters": "должен содержать минимум 4 символа",
    "value is not a valid enumeration member": "Недопустимая роль",
    "field required": "обязательное поле",
  };

  export const processorErrorMessages = (detail) => {
    if (!Array.isArray(detail)) return detail;

    return detail
    .map((error) => {
        const field = error.loc[error.loc.length - 1];
        let message = error.msg;
        const localized = Object.entries(errorLocalization).find(([key]) =>
        message.includes(key)
        );
        if (localized) {
        message = `${field} ${localized[1]}`;
        } else if (message === "invalid credentials") {
        message = "Неверные учетные данные";
        }
        return message;
    })
    .join("; ");
    };
