import { HideShutDownPlugin } from './plugins';
import { SessionManagementPlugin } from './plugins';
import { ResourceUsagePlugin } from './plugins';
import { GitClonePlugin } from './plugins';
import { PerformanceMeteringPlugin } from './plugins';

export default [
  HideShutDownPlugin,
  SessionManagementPlugin,
  ResourceUsagePlugin,
  GitClonePlugin,
  PerformanceMeteringPlugin,
];
