export const generateChatId = (): string => {
  return `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};

export const countWords = (text: string): number => {
  return text.trim() ? text.trim().split(/\s+/).length : 0;
};
