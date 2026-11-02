import { HugeiconsIcon } from '@hugeicons/react';
import {
  ArrowUpRight01Icon,
  ArrowDown01Icon,
  ArrowRight01Icon,
  Globe02Icon,
  Menu01Icon,
  Cancel01Icon,
  Database01Icon,
  InformationCircleIcon,
  PlayIcon,
  PauseIcon,
  ArrowReloadHorizontalIcon,
  Calendar03Icon,
  UserGroupIcon,
  Tick02Icon,
  GithubIcon,
} from '@hugeicons/core-free-icons';

// Every interface icon uses Hugeicons' Stroke Rounded family and the same weight.
function renderIcon(icon) {
  return function Icon({ size = 20, strokeWidth = 1.5, ...props }) {
    return (
      <HugeiconsIcon
        icon={icon}
        size={size}
        strokeWidth={strokeWidth}
        color="currentColor"
        aria-hidden="true"
        focusable="false"
        {...props}
      />
    );
  };
}
export const ArrowUpRight = renderIcon(ArrowUpRight01Icon);
export const ArrowDown = renderIcon(ArrowDown01Icon);
export const ArrowRight = renderIcon(ArrowRight01Icon);
export const Globe2 = renderIcon(Globe02Icon);
export const Menu = renderIcon(Menu01Icon);
export const X = renderIcon(Cancel01Icon);
export const Database = renderIcon(Database01Icon);
export const Info = renderIcon(InformationCircleIcon);
export const Play = renderIcon(PlayIcon);
export const Pause = renderIcon(PauseIcon);
export const RotateCcw = renderIcon(ArrowReloadHorizontalIcon);
export const Calendar = renderIcon(Calendar03Icon);
export const Users = renderIcon(UserGroupIcon);
export const Check = renderIcon(Tick02Icon);
export const GitHub = renderIcon(GithubIcon);
