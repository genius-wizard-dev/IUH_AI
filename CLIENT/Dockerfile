# Stage 1: Build ứng dụng
FROM oven/bun:1.1-alpine AS builder

WORKDIR /app

# Copy file package.json và bun.lockb để cài dependencies
COPY package.json bun.lockb ./
RUN bun install

# Copy source code (không bao gồm node_modules nhờ .dockerignore)
COPY . .

# Build ứng dụng
RUN bun run build

# Stage 2: Chạy ứng dụng
FROM oven/bun:1.1-alpine

WORKDIR /app

# Copy chỉ thư mục dist từ stage builder
COPY --from=builder /app/dist ./dist

# Cài serve để chạy file tĩnh (nếu dùng serve)
RUN bun install -g serve

# Expose cổng
EXPOSE 3000

# Chạy ứng dụng
CMD ["bunx", "serve", "-s", "dist", "-l", "3000"]
