import { PanelPlugin } from '@grafana/data';
import { ChatPanel } from './ChatPanel';

export const plugin = new PanelPlugin<{}>(ChatPanel)
