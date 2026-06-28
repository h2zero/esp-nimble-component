idf_build_get_property(target IDF_TARGET)

if(${target} STREQUAL "linux")
    return()
endif()

# Normalize IDF_PATH
file(TO_CMAKE_PATH "$ENV{IDF_PATH}" IDF_PATH_NORM)
set(SYSTEM_BT_DIR "${IDF_PATH_NORM}/components/bt")

if(CONFIG_IDF_TARGET_ESP32S3)
    set(target_name "esp32c3")
elseif(CONFIG_IDF_TARGET_ESP32C61)
    set(target_name "esp32c6")
else()
    set(target_name "${idf_target}")
endif()

if(CONFIG_BT_ENABLED)
    set(srcs "")
    set(include_dirs "")
    set(priv_include_dirs "")
    set(ldscripts "${SYSTEM_BT_DIR}/linker_common.lf")

    if(CONFIG_BT_CONTROLLER_ENABLED)
        list(APPEND include_dirs "${SYSTEM_BT_DIR}/include/${target_name}/include")

        if(CONFIG_IDF_TARGET_ESP32)
            list(APPEND srcs
                "${SYSTEM_BT_DIR}/controller/esp32/bt.c"
                "${SYSTEM_BT_DIR}/controller/esp32/hli_api.c"
                "${SYSTEM_BT_DIR}/controller/esp32/hli_vectors.S"
            )
            list(APPEND ldscripts "${SYSTEM_BT_DIR}/linker_rw_bt_controller.lf")
        elseif(CONFIG_IDF_TARGET_ESP32C3 OR CONFIG_IDF_TARGET_ESP32S3)
            list(APPEND srcs "${SYSTEM_BT_DIR}/controller/${target_name}/bt.c")
            list(APPEND ldscripts "${SYSTEM_BT_DIR}/linker_rw_bt_controller.lf")
        elseif(CONFIG_IDF_TARGET_ESP32C2)
            list(APPEND srcs
                "${SYSTEM_BT_DIR}/controller/esp32c2/bt.c"
                "${SYSTEM_BT_DIR}/controller/esp32c2/ble.c"
            )
            if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
                list(APPEND srcs "${SYSTEM_BT_DIR}/controller/esp32c2/dummy.c")
            endif()
            list(APPEND ldscripts "${SYSTEM_BT_DIR}/linker_esp32c2.lf")
        else()
            list(APPEND srcs
                "${SYSTEM_BT_DIR}/controller/${target_name}/bt.c"
                "${SYSTEM_BT_DIR}/controller/${target_name}/ble.c"
            )
            list(APPEND ldscripts "${SYSTEM_BT_DIR}/linker_esp_ble_controller.lf")
        endif()
    endif()

    list(APPEND include_dirs
        "${SYSTEM_BT_DIR}/common/osi/include"
        "${SYSTEM_BT_DIR}/common/api/include/api"
        "${SYSTEM_BT_DIR}/common/btc/profile/esp/blufi/include"
        "${SYSTEM_BT_DIR}/common/btc/profile/esp/include"
        "${SYSTEM_BT_DIR}/common/hci_log/include"
        "${SYSTEM_BT_DIR}/common/ble_log/include"
    )

    list(APPEND priv_include_dirs
        "${SYSTEM_BT_DIR}/common/btc/include"
        "${SYSTEM_BT_DIR}/common/include"
        "${SYSTEM_BT_DIR}/porting/mem"
        "${SYSTEM_BT_DIR}/porting/include"
        "${SYSTEM_BT_DIR}/porting/transport/include"
    )

    list(APPEND srcs
        "${SYSTEM_BT_DIR}/common/btc/core/btc_alarm.c"
        "${SYSTEM_BT_DIR}/common/api/esp_blufi_api.c"
        "${SYSTEM_BT_DIR}/common/hci_log/bt_hci_log.c"
        "${SYSTEM_BT_DIR}/common/btc/core/btc_manage.c"
        "${SYSTEM_BT_DIR}/common/btc/core/btc_task.c"
        "${SYSTEM_BT_DIR}/common/btc/profile/esp/blufi/blufi_prf.c"
        "${SYSTEM_BT_DIR}/common/btc/profile/esp/blufi/blufi_protocol.c"
        "${SYSTEM_BT_DIR}/common/osi/alarm.c"
        "${SYSTEM_BT_DIR}/common/osi/allocator.c"
        "${SYSTEM_BT_DIR}/common/osi/buffer.c"
        "${SYSTEM_BT_DIR}/common/osi/config.c"
        "${SYSTEM_BT_DIR}/common/osi/fixed_queue.c"
        "${SYSTEM_BT_DIR}/common/osi/pkt_queue.c"
        "${SYSTEM_BT_DIR}/common/osi/fixed_pkt_queue.c"
        "${SYSTEM_BT_DIR}/common/osi/future.c"
        "${SYSTEM_BT_DIR}/common/osi/hash_functions.c"
        "${SYSTEM_BT_DIR}/common/osi/hash_map.c"
        "${SYSTEM_BT_DIR}/common/osi/list.c"
        "${SYSTEM_BT_DIR}/common/osi/mutex.c"
        "${SYSTEM_BT_DIR}/common/osi/thread.c"
        "${SYSTEM_BT_DIR}/common/osi/osi.c"
        "${SYSTEM_BT_DIR}/common/osi/semaphore.c"
        "${SYSTEM_BT_DIR}/porting/mem/bt_osi_mem.c"
        "${SYSTEM_BT_DIR}/common/ble_log/ble_log_spi_out.c"
    )

    if(CONFIG_BT_NIMBLE_ENABLED)
        set(NIMBLE_ROOT "${CMAKE_CURRENT_LIST_DIR}/host/nimble")

        list(APPEND include_dirs
            "${NIMBLE_ROOT}/nimble/nimble/host/include"
            "${NIMBLE_ROOT}/nimble/nimble/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ans/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/bas/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/dis/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/gap/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/gatt/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/hr/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/htp/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ias/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/ipss/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/lls/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/prox/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/cts/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/tps/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/hid/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/sps/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/services/cte/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/util/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/ram/include"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/include"
            "${NIMBLE_ROOT}/nimble/porting/nimble/include"
            "${NIMBLE_ROOT}/port/include"
            "${NIMBLE_ROOT}/nimble/nimble/transport/include"
            "${NIMBLE_ROOT}/esp-hci/include"
            "${SYSTEM_BT_DIR}/porting/include"
            "${SYSTEM_BT_DIR}/porting/transport/include"
        )

        file(GLOB nimble_host_srcs "${NIMBLE_ROOT}/nimble/nimble/host/src/*.c")
        file(GLOB nimble_services_srcs "${NIMBLE_ROOT}/nimble/nimble/host/services/*/src/*.c")
        list(FILTER nimble_host_srcs EXCLUDE REGEX ".*/ble_sm_alg\\.c$")
        list(FILTER nimble_host_srcs EXCLUDE REGEX ".*/ble_aes_ccm\\.c$")
        list(FILTER nimble_services_srcs EXCLUDE REGEX ".*/services/bleuart/.*")

        set(nimble_crypto_srcs
            "${NIMBLE_ROOT}/nimble/nimble/host/src/ble_sm_alg.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/src/ble_aes_ccm.c"
        )

        if(NOT (CONFIG_BT_LE_CRYPTO_STACK_MBEDTLS OR CONFIG_BT_NIMBLE_CRYPTO_STACK_MBEDTLS))
            list(APPEND include_dirs "${NIMBLE_ROOT}/nimble/ext/tinycrypt/include")
            file(GLOB nimble_tinycrypt_srcs "${NIMBLE_ROOT}/nimble/ext/tinycrypt/src/*.c")
            list(APPEND nimble_crypto_srcs ${nimble_tinycrypt_srcs})
        elseif(NOT CONFIG_MBEDTLS_VER_4_X_SUPPORT)
            list(APPEND include_dirs
                "${IDF_PATH_NORM}/components/mbedtls/mbedtls/include"
                "${IDF_PATH_NORM}/components/mbedtls/port/include"
            )
        else()
            list(APPEND include_dirs
                "${IDF_PATH_NORM}/components/mbedtls/mbedtls/tf-psa-crypto/include"
                "${IDF_PATH_NORM}/components/mbedtls/mbedtls/tf-psa-crypto/drivers/builtin/include"
            )
        endif()

        list(APPEND srcs
            "${NIMBLE_ROOT}/nimble/nimble/transport/src/transport.c"
            ${nimble_host_srcs}
            ${nimble_services_srcs}
            ${nimble_crypto_srcs}
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/endian.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_mempool.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/mem.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_mbuf.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/os_msys_init.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/util/src/addr.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/ram/src/ble_store_ram.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/src/ble_store_config.c"
            "${NIMBLE_ROOT}/nimble/nimble/host/store/config/src/ble_store_nvs.c"
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/src/nimble_port_freertos.c"
            "${NIMBLE_ROOT}/nimble/porting/nimble/src/nimble_port.c"
            "${NIMBLE_ROOT}/port/src/nvs_port.c"
        )
    endif()

    if(NOT CONFIG_BT_LE_CONTROLLER_NPL_OS_PORTING_SUPPORT)
        list(APPEND srcs
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/src/npl_os_freertos.c"
        )

        list(APPEND include_dirs
            "${NIMBLE_ROOT}/nimble/porting/npl/freertos/include"
        )

    else()
        list(APPEND srcs
            "${NIMBLE_ROOT}/nimble/nimble/transport/esp_ipc/src/hci_esp_ipc.c"
            "${SYSTEM_BT_DIR}/porting/transport/src/hci_transport.c"
            "${SYSTEM_BT_DIR}/porting/transport/driver/vhci/hci_driver_nimble.c"
            "${SYSTEM_BT_DIR}/porting/npl/freertos/src/npl_os_freertos.c"
        )

        list(APPEND include_dirs
            "${SYSTEM_BT_DIR}/porting/npl/freertos/include"
        )

    endif()

    if(CONFIG_BT_NIMBLE_LEGACY_VHCI_ENABLE AND CONFIG_BT_CONTROLLER_ENABLED)
        list(APPEND srcs
            "${NIMBLE_ROOT}/esp-hci/src/esp_nimble_hci.c"
            "${NIMBLE_ROOT}/nimble/nimble/transport/esp_ipc_legacy/src/hci_esp_ipc_legacy.c"
            "${SYSTEM_BT_DIR}/common/btc/profile/esp/blufi/nimble_host/esp_blufi.c"
        )
        list(APPEND include_dirs ${nimble_hci_include_dirs})
    endif()

    idf_component_register(
        SRCS ${srcs}
        INCLUDE_DIRS ${include_dirs}
        PRIV_INCLUDE_DIRS ${priv_include_dirs}
        REQUIRES esp_timer esp_wifi
        PRIV_REQUIRES nvs_flash soc esp_pm esp_phy esp_coex mbedtls esp_driver_uart vfs esp_ringbuf esp_driver_spi esp_driver_gpio
        LDFRAGMENTS ${ldscripts}
    )

    target_include_directories(${COMPONENT_LIB} PUBLIC
        "${IDF_PATH_NORM}/components/esp_timer/include"
        "${IDF_PATH_NORM}/components/esp_phy/include"
        "${IDF_PATH_NORM}/components/esp_wifi/include"
        "${IDF_PATH_NORM}/components/esp_event/include"
        "${IDF_PATH_NORM}/components/esp_pm/include"
        "${IDF_PATH_NORM}/components/esp_coex/include"
        "${IDF_PATH_NORM}/components/nvs_flash/include"
        "${IDF_PATH_NORM}/components/esp_partition/include"
        "${IDF_PATH_NORM}/components/esp_blockdev/include"
        "${IDF_PATH_NORM}/components/esp_driver_spi/include"
        "${IDF_PATH_NORM}/components/esp_driver_gpio/include"
        "${IDF_PATH_NORM}/components/esp_hal_gpspi/include"
    )

    if(CONFIG_IDF_TARGET_ESP32)
        set_source_files_properties("${SYSTEM_BT_DIR}/controller/esp32/hli_vectors.S" PROPERTIES COMPILE_FLAGS "-x assembler-with-cpp")
    endif()

    target_compile_options(${COMPONENT_LIB} PRIVATE -Wno-implicit-fallthrough -Wno-unused-const-variable -Wno-format)
    target_compile_definitions(${COMPONENT_LIB} PRIVATE MBEDTLS_CONFIG_FILE="${IDF_PATH_NORM}/components/mbedtls/port/include/mbedtls/esp_config.h")

    if(CONFIG_IDF_TARGET_ESP32)
        target_link_directories(${COMPONENT_LIB} INTERFACE "${SYSTEM_BT_DIR}/controller/lib_esp32/esp32")
        target_link_libraries(${COMPONENT_LIB} PUBLIC btdm_app)
        target_link_libraries(${COMPONENT_LIB} INTERFACE "-u ld_include_hli_vectors_bt")

        add_prebuilt_library(bt_btdm_app "${SYSTEM_BT_DIR}/controller/lib_esp32/esp32/libbtdm_app.a")
        target_link_libraries(${COMPONENT_LIB} PRIVATE bt_btdm_app)
        target_link_options(${COMPONENT_LIB} INTERFACE "SHELL:-u ld_include_hli_vectors_bt")

    elseif(CONFIG_IDF_TARGET_ESP32C3)
        if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
            set(lib_name "btdm_app_flash")
        else()
            set(lib_name "btdm_app")
        endif()

        add_prebuilt_library(bt_btdm_app
                             "${SYSTEM_BT_DIR}/controller/lib_esp32c3_family/esp32c3/lib${lib_name}.a")
        target_link_libraries(${COMPONENT_LIB} PRIVATE bt_btdm_app)

    elseif(CONFIG_IDF_TARGET_ESP32S3)
        if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY)
            set(lib_name "btdm_app_flash")
        else()
            set(lib_name "btdm_app")
        endif()

        add_prebuilt_library(bt_btdm_app
                             "${SYSTEM_BT_DIR}/controller/lib_esp32c3_family/esp32s3/lib${lib_name}.a")
        target_link_libraries(${COMPONENT_LIB} PRIVATE bt_btdm_app)

    elseif(CONFIG_BT_CONTROLLER_ENABLED)
        if(CONFIG_BT_LE_CONTROLLER_LOG_WRAP_PANIC_HANDLER_ENABLE)
            target_link_options(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=esp_panic_handler")
        endif()
        if(CONFIG_BT_BLE_LOG_UHCI_OUT_ENABLED)
            target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_tx_chars")
            target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_write_bytes")
            target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_write_bytes_with_break")
        endif()
        if(DEFINED CONFIG_BLE_LOG_PRPH_UART_DMA_PORT)
            if(CONFIG_BLE_LOG_PRPH_UART_DMA_PORT EQUAL 0)
                target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_tx_chars")
                target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_write_bytes")
                target_link_libraries(${COMPONENT_LIB} INTERFACE "-Wl,--wrap=uart_write_bytes_with_break")
            endif()
        endif()

        if(CONFIG_IDF_TARGET_ESP32C6)
            add_prebuilt_library(libble_app
                "${SYSTEM_BT_DIR}/controller/lib_esp32c6/esp32c6-bt-lib/esp32c6/libble_app.a"
                REQUIRES esp_phy)
        elseif(CONFIG_IDF_TARGET_ESP32C61)
            add_prebuilt_library(libble_app
                "${SYSTEM_BT_DIR}/controller/lib_esp32c6/esp32c6-bt-lib/esp32c61/libble_app.a"
                REQUIRES esp_phy)
        else()
            if(CONFIG_BT_CTRL_RUN_IN_FLASH_ONLY AND CONFIG_IDF_TARGET_ESP32C2)
                add_prebuilt_library(libble_app
                    "${SYSTEM_BT_DIR}/controller/lib_${target_name}/${target_name}-bt-lib/libble_app_flash.a"
                    REQUIRES esp_phy)
            else()
                add_prebuilt_library(libble_app
                    "${SYSTEM_BT_DIR}/controller/lib_${target_name}/${target_name}-bt-lib/libble_app.a"
                    REQUIRES esp_phy)
            endif()
        endif()
        target_link_libraries(${COMPONENT_LIB} PRIVATE libble_app)
    endif()

else()
    idf_component_register()
endif()
