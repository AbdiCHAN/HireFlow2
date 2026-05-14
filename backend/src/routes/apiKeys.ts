import { Router } from 'express';
import { ApiKeyModel } from '../models/ApiKey.ts';
import { authenticateToken } from '../middleware/auth.ts';

const router = Router();
let apiKeyModel: ApiKeyModel;

export function setApiKeyModel(db: any) {
  apiKeyModel = ApiKeyModel.create(db);
}

router.get('/', authenticateToken, async (req, res) => {
  try {
    const keys = await apiKeyModel.listByUser(req.user!.id);
    res.json({ data: keys });
  } catch (error) {
    console.error('List API keys error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.post('/', authenticateToken, async (req, res) => {
  try {
    const name = typeof req.body?.name === 'string' ? req.body.name : 'HireFlow API Key';
    const key = await apiKeyModel.create(req.user!.id, name);
    res.status(201).json({
      message: 'API key created. Copy it now; it will not be shown again.',
      data: key,
    });
  } catch (error) {
    console.error('Create API key error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

router.delete('/:id', authenticateToken, async (req, res) => {
  try {
    const id = Number(req.params.id);
    if (!Number.isFinite(id)) {
      return res.status(400).json({ error: 'Invalid API key ID' });
    }

    const revoked = await apiKeyModel.revoke(req.user!.id, id);
    if (!revoked) {
      return res.status(404).json({ error: 'API key not found' });
    }

    res.json({ message: 'API key revoked successfully' });
  } catch (error) {
    console.error('Revoke API key error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;
