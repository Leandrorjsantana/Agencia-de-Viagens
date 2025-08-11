// frontend/src/config.js

/**
 * Configuração central do frontend.
 * Aqui definimos o endereço base do backend e funções auxiliares.
 */
export const BACKEND_URL =
  process.env.VUE_APP_BACKEND_URL || "http://127.0.0.1:8000";

/**
 * Monta uma URL absoluta para imagens e documentos.
 * - Se já for absoluta, retorna como está.
 * - Se for relativa, concatena com BACKEND_URL.
 */
export function getMediaUrl(path) {
  if (!path) return "";
  if (path.startsWith("http://") || path.startsWith("https://")) {
    return path;
  }
  return `${BACKEND_URL}${path}`;
}
