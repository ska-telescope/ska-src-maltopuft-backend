=====
Usage
=====

The MALTOPUFT API currently provides four main features:

1. Fast transient candidate creation
2. Fast transient candidate querying
3. Cross-matching fast transient candidates with known pulsars
4. Fast transient candidate labelling

.. tip::

    There are plans to support all the features listed above with periodicity candidates in the future.

The following documentation gives a brief overview of these features.

Create a single pulse candidate
===============================

In terms of MALTOPUFT, a "candidate" can have either a single pulse or a periodic candidate. Organising the data in this way helps when cross-matching single pulse and periodicity candidates with known sources, as only the parent candidate objects need to be queried. In general, candidate creation is not considered to be the users responsibility. Candidate data and their associated metadata is intended to be consumed from various telescope data archives.

At this point in time, it is required to make two API requests to create a single pulse candidate. The first creates the parent candidate:

.. code-block::

    curl -X 'POST' \
      'http://localhost:8000/v1/candle/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "ra": "53h92m48s",
      "dec": "1d05m66s",
      "dm": 1,
      "snr": 1,
      "width": 1,
      "observed_at": "2024-09-12T13:35:30.917Z",
      "beam_id": 10
    }'

.. warning::
    The candidate ``beam_id`` is a non-nullable attribute. This means that observation metadata must exist to create a candidate.

The second creates the single pulse candidate:

.. code-block::

    curl -X 'POST' \
      'http://localhost:8000/v1/candle/sp' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "plot_path": "/path/to/file",
      "candidate_id": 1
    }'

Fast transient candidate querying
=================================

Single pulse candidates can be retrieved by ascending ``candidate.observed_at`` as follows.

.. code-block:: bash

    curl -X 'GET' \
      'http://localhost:8000/v1/candle/sp?limit=2' \
      -H 'accept: application/json'

    ...

    [
      {
        "id": 5859,
        "plot_path": "5859.jpg",
        "candidate_id": 5859,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 5859,
          "dm": 301.167,
          "snr": 8.02,
          "width": 195.996,
          "ra": "53h92m48s",
          "dec": "1d05m66s",
          "beam_id": 3,
          "observed_at": "2023-12-13T20:15:11.898000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      },
      {
        "id": 1784,
        "plot_path": "1784.jpg",
        "candidate_id": 1784,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 1784,
          "dm": 215.514,
          "snr": 8.89,
          "width": 195.996,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 3,
          "observed_at": "2023-12-13T20:15:11.927000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      },
    ]

When no query parameters are specified, the default behaviour is to fetch single pulse candidates from the earliest observation in ascending time order. If order query parameters are specified, single pulse candidates are selected and ordered by descending observeration time in order to return the *most recent* candidates.

If the ``latest`` query parameter is set to ``true``, only candidates from the most recent observation are returned (in ascending time order):

.. code-block:: bash

    curl -X 'GET' \
      'http://localhost:8000/v1/candle/sp?latest=true' \
      -H 'accept: application/json'
    
    ...

    [
      {
        "id": 8969,
        "plot_path": "tpn-0-12_1702540743166/60292.332245239406_DM_323.58_beam_390C.jpg",
        "candidate_id": 8969,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 8969,
          "dm": 323.578,
          "snr": 9.14,
          "width": 195.996,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 5469,
          "observed_at": "2023-12-14T07:58:25.989000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      },
      {
        "id": 492,
        "plot_path": "tpn-0-12_1702540742276/60292.3322456931_DM_308.54_beam_389C.jpg",
        "candidate_id": 492,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 492,
          "dm": 308.535,
          "snr": 9.04,
          "width": 195.996,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 5468,
          "observed_at": "2023-12-14T07:58:26.028000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      },
      {
        "id": 1240,
        "plot_path": "tpn-0-12_1702540738189/60292.3322463737_DM_296.87_beam_395C.jpg",
        "candidate_id": 1240,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 1240,
          "dm": 296.869,
          "snr": 8.5,
          "width": 195.996,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 5474,
          "observed_at": "2023-12-14T07:58:26.087000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      },
      {
        "id": 2838,
        "plot_path": "tpn-0-12_1702540739059/60292.3322603247_DM_314.68_beam_395C.jpg",
        "candidate_id": 2838,
        "created_at": "2024-09-12T13:49:41.393458",
        "updated_at": "2024-09-12T13:49:41.393458",
        "candidate": {
          "id": 2838,
          "dm": 314.675,
          "snr": 8.87,
          "width": 195.996,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 5474,
          "observed_at": "2023-12-14T07:58:27.292000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        }
      }
    ]

The number of single pulses matching any query parameters can be retrieved with the ``/count`` endpoint. For example, counting the number of single pulses in the latest observation response returned in the above code snippet:

.. code-block ::

    curl -X 'GET' \
      'http://localhost:8000/v1/candle/sp/count?latest=true' \
      -H 'accept: application/json'

    ...

    4

Cross-matching fast transient candidates with known pulsars
===========================================================

Known pulsars are retrieved from the ATNF pulsar catalogue. This feature prepares a list of known sources lying inside a cone with the specified radius about the centre of an observation. The observation metadata and list of known sources are then included in the response.

To retrieve a list of three known sources:

.. code-block:: bash

    curl -X 'GET' \
      'http://localhost:8000/v1/catalogues/pulsars?limit=3' \
      -H 'accept: application/json'


    ...

    [
      {
        "id": 1,
        "name": "J0002+6216",
        "dm": 218.6,
        "width": null,
        "ra": "00h02m58s",
        "dec": "62d16m09s",
        "period": 0.11536356826797663,
        "created_at": "2024-09-12T13:51:00.955703",
        "updated_at": "2024-09-12T13:51:00.955703"
      },
      {
        "id": 2,
        "name": "J0006+1834",
        "dm": 11.4,
        "width": 40,
        "ra": "00h06m04s",
        "dec": "18d34m59s",
        "period": 0.69374767047,
        "created_at": "2024-09-12T13:51:00.955703",
        "updated_at": "2024-09-12T13:51:00.955703"
      },
      {
        "id": 3,
        "name": "J0007+7303",
        "dm": null,
        "width": null,
        "ra": "00h07m01s",
        "dec": "73d03m07s",
        "period": 0.3158731908527248,
        "created_at": "2024-09-12T13:51:00.955703",
        "updated_at": "2024-09-12T13:51:00.955703"
      }
    ]

The "cross-matched" results can be returned as follows:

.. code-block:: bash

    curl -X 'GET' \
    'http://localhost:8000/v1/obs/sources?radius=1&id=2' \
    -H 'accept: application/json'

    ...

    [
      {
        "observation": {
          "id": 2,
          "t_min": "2023-12-13T20:19:03",
          "t_max": "2023-12-13T20:21:22",
          "s_ra": "6h30m49s",
          "s_dec": "-28d34m42s",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458"
        },
        "sources": [
          {
            "id": 324,
            "name": "B0628-28",
            "dm": 34.425,
            "width": 63,
            "ra": "06h30m49s",
            "dec": "-28d34m42s",
            "period": 1.2444185961512455,
            "created_at": "2024-09-12T13:51:00.955703",
            "updated_at": "2024-09-12T13:51:00.955703"
          }
        ]
      }
    ]

Fast transient candidate labelling
==================================

Candidates can be labelled with "label entities". Label entites can be created with:

.. code-block:: bash

    curl -X 'POST' \
      'http://localhost:8000/v1/labels/entity' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "type": "RFI",
      "css_color": "cccccc"
    }'

.. warning::

    Although create label entity API exists, the entity type must be unique and configured as an allowed value in the application, meaning that arbitrary label entities can't be created in the application.

Once the label entities have been created, labels can be assigned to candidates with:

.. code-block:: bash

    curl -X 'POST' \
      'http://localhost:8000/v1/labels/' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -H 'Bearer your-token' \
      -d '{
      "candidate_id": 1,
      "entity_id": 1
    }'

Labels can be retrieved with:

.. code-block:: bash

    curl -X 'GET' \
      'http://localhost:8000/v1/labels/' \
      -H 'accept: application/json'

    ...

    [
      {
        "id": 2,
        "labeller_id": 1,
        "candidate_id": 1,
        "entity_id": 1,
        "created_at": "2024-09-12T16:24:04.801953",
        "updated_at": "2024-09-12T16:24:04.801953",
        "candidate": {
          "id": 1,
          "dm": 56.488,
          "snr": 10.06,
          "width": 12.5829,
          "ra": "5h19m58s",
          "dec": "1d05m66s",
          "beam_id": 4270,
          "observed_at": "2023-12-14T02:44:32.473000",
          "created_at": "2024-09-12T13:49:41.393458",
          "updated_at": "2024-09-12T13:49:41.393458",
          "sp_candidate": {
            "id": 1,
            "plot_path": "1.jpg",
            "candidate_id": 1,
            "created_at": "2024-09-12T13:49:41.393458",
            "updated_at": "2024-09-12T13:49:41.393458"
          }
        },
        "entity": {
          "id": 1,
          "type": "RFI",
          "css_color": "cccccc",
          "created_at": "2024-09-12T16:15:56.077562",
          "updated_at": "2024-09-12T16:15:56.077562"
        },
        "labeller": {
          "id": 1,
          "uuid": "your-uuid",
          "username": "your-username",
          "is_admin": false,
          "created_at": "2024-09-12T16:23:53.990595",
          "updated_at": "2024-09-12T16:23:53.990595"
        }
      }
    ]
