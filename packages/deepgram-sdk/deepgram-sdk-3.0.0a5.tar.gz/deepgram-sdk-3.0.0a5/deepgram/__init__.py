# Copyright 2023 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

# version
__version__ = "v3.0.0-alpha.5"

# entry point for the deepgram python sdk
from .client import DeepgramClient, DeepgramApiKeyError
from .options import DeepgramClientOptions

# live
from .clients.live.enums import LiveTranscriptionEvents
from .clients.live.client import LiveClient, LegacyLiveClient, LiveOptions

# prerecorded
from .clients.prerecorded.client import (
    PreRecordedClient,
    PrerecordedOptions,
    PrerecordedSource,
    FileSource,
    UrlSource,
)

# manage
from .clients.manage.client import (
    ManageClient,
    ProjectOptions,
    KeyOptions,
    ScopeOptions,
    InviteOptions,
    UsageRequestOptions,
    UsageSummaryOptions,
    UsageFieldsOptions,
)

# utilities
from .audio.microphone.microphone import Microphone
