import { createHash, randomBytes } from 'crypto';
import { Database } from 'sqlite';

export interface ApiKeyRecord {
  id?: number;
  userId: number;
  name: string;
  keyHash: string;
  keyPrefix: string;
  createdAt?: string;
  lastUsedAt?: string | null;
  revokedAt?: string | null;
}

export interface CreatedApiKey extends Omit<ApiKeyRecord, 'keyHash'> {
  key: string;
}

const hashKey = (key: string) => {
  return createHash('sha256').update(key).digest('hex');
};

const publicShape = (row: any) => ({
  id: row.id,
  userId: row.userId,
  name: row.name,
  keyPrefix: row.keyPrefix,
  createdAt: row.createdAt,
  lastUsedAt: row.lastUsedAt,
  revokedAt: row.revokedAt,
});

export class ApiKeyModel {
  private db: Database;

  constructor(db: Database) {
    this.db = db;
  }

  static create(db: Database): ApiKeyModel {
    return new ApiKeyModel(db);
  }

  async create(userId: number, name = 'HireFlow API Key'): Promise<CreatedApiKey> {
    const key = `hf_${randomBytes(24).toString('base64url')}`;
    const keyHash = hashKey(key);
    const keyPrefix = `${key.slice(0, 8)}...`;

    const result = await this.db.run(
      `INSERT INTO api_keys (user_id, name, key_hash, key_prefix)
       VALUES (?, ?, ?, ?)`,
      [userId, name.trim() || 'HireFlow API Key', keyHash, keyPrefix]
    );

    return {
      id: result.lastID,
      userId,
      name: name.trim() || 'HireFlow API Key',
      key,
      keyPrefix,
      createdAt: new Date().toISOString(),
      lastUsedAt: null,
      revokedAt: null,
    };
  }

  async listByUser(userId: number): Promise<Omit<ApiKeyRecord, 'keyHash'>[]> {
    const rows = await this.db.all(
      `SELECT id, user_id as userId, name, key_prefix as keyPrefix,
              created_at as createdAt, last_used_at as lastUsedAt,
              revoked_at as revokedAt
       FROM api_keys
       WHERE user_id = ?
       ORDER BY created_at DESC`,
      [userId]
    );

    return rows.map(publicShape);
  }

  async revoke(userId: number, id: number): Promise<boolean> {
    const result = await this.db.run(
      `UPDATE api_keys
       SET revoked_at = ?
       WHERE id = ? AND user_id = ? AND revoked_at IS NULL`,
      [new Date().toISOString(), id, userId]
    );

    return (result.changes || 0) > 0;
  }

  async verify(key: string): Promise<ApiKeyRecord | null> {
    const row = await this.db.get(
      `SELECT id, user_id as userId, name, key_hash as keyHash,
              key_prefix as keyPrefix, created_at as createdAt,
              last_used_at as lastUsedAt, revoked_at as revokedAt
       FROM api_keys
       WHERE key_hash = ? AND revoked_at IS NULL`,
      [hashKey(key)]
    );

    if (!row) return null;

    await this.db.run(
      `UPDATE api_keys SET last_used_at = ? WHERE id = ?`,
      [new Date().toISOString(), row.id]
    );

    return row as ApiKeyRecord;
  }
}

