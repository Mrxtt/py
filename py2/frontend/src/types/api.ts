/**
 * API 响应类型定义
 */

/**
 * 统一 API 响应接口
 */
export interface ApiResponse<T = any> {
  code: number;
  message: string;
  data: T;
}

/**
 * 分页数据接口
 */
export interface PageData<T = any> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  pages: number;
}

/**
 * 分页响应接口
 */
export interface PageResponse<T = any> {
  code: number;
  message: string;
  data: PageData<T>;
}

/**
 * 错误响应接口
 */
export interface ErrorResponse {
  code: number;
  message: string;
  detail?: string;
}
